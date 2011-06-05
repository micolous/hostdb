#from django.conf import settings
#from models import *
#import models
from os import path
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from hostdb.hdb.models import *
import traceback
import sys
from easyzone import easyzone
from easyzone.zone_check import ZoneCheck
#read the user input, to determine the zone name, and file to be read.

#filename = 'firstyear.id.au.zone'
#zname = 'firstyear.id.au'

class Command(BaseCommand):
	can_import_settings = True
	help = "Import dns zone file to database and bring it under hdb control."
	option_list = BaseCommand.option_list + (
		make_option('-f', '--file',
			dest='filename',
			metavar = 'FILE',
			default = None,
			help='dns zone file to import'),
		make_option('-z', '--zonename',
			dest='zonename',
			metavar = 'ZONE',
			default = None,
			help='specify the zone name this zone file belongs to. If ommitted, defaults to name of file.'),
		make_option('-k', '--keyfile',
			dest='keyfile',
			metavar = 'KEY',
			default = '/etc/named/rndc.key',
			help='specify the keyfile where your RNDC key is stored on the DNS server.'),
		make_option('-c', '--checkzone',
			dest='checkzone',
			metavar = 'CHECK',
			default = '/usr/sbin/named-checkzone',
			help='specify the path to the ISC-BIND named-checkzone binary'),
	
		)

	def handle(self, filename, zonename, keyfile, checkzone, *args, **options):
		if not filename:
			print "Must supply valid filename"
			exit(-1)
		if not zonename:
			print "Must supply valid zonename"
			exit(-1)
		if zonename[-1] != '.':
			zonename += '.'
		# Check the zone
		c = ZoneCheck(checkzone=checkzone)
		if not c.isValid(zonename, filename):
			print "Invalid zone"
			exit(-1)

		z = easyzone.zone_from_file(zonename, filename)
		
		if len(DNSZone.objects.filter(zonename=zonename)) == 0:
			dnsz = DNSZone()
			dnsz.zonename = zonename
			dnsz.ttl = z.root.soa.minttl
			dnsz.rndckey = keyfile
			#fk email to a user?
			dnsz.email = 'william.e.brown@adelaide.edu.au'
			dnsz.serial = z.root.soa.serial
			dnsz.refresh = z.root.soa.refresh
			dnsz.retry = z.root.soa.retry
			dnsz.expire = z.root.soa.expire
			dnsz.minimum = z.root.soa.minttl
			dnsz.save()
		else:
			dnsz = DNSZone.objects.get(zonename=zonename)
		
		#We want to populate the A and AAAA records first, else we wont have integrity for the other records.
		for rtype in ('A', 'AAAA', 'MX', 'PTR', 'TXT', 'SRV', 'CNAME', 'NS', 'HINFO'):
			for r in z.names:
				try:
					for rec in z.names[r].records(rtype).items:
						if rtype != 'MX':
							print '%s : %s : %s' %( r , rtype , rec)
						else:
							print '%s : %s : %s %s ' % ( r , rtype , rec[0] , rec[1])
						#Check if the record exists or not
						if len(DNSRecord.objects.filter(type=rtype,record=rec,fqdn=r)) == 0:
							dr = DNSRecord()
							dr.zone = dnsz
							dr.type = rtype
							if rtype == 'MX':
								rec = '%s %s' % rec
							dr.record = rec
							dr.ttl = dnsz.ttl
							dr.fqdn = r
							if rtype in ('A', 'AAAA'):
								try:
									a = Address.objects.get(address=rec)
								except Address.DoesNotExist:
									a = Address()
									a.host = None
									a.type = 6
									if rtype == 'A':
										a.type = 4
									a.vlan = 0
									a.hwid = None
									a.address = rec
									a.save()
								dr.address = a
							dr.save()
							if rtype in ('MX', 'CNAME', 'NS', 'PTR', 'TXT', 'SRV'):
								test = rec.split(' ')[-1]
								#We should also split the rec if possible - last field is our related name in SRV / MX
								related = DNSRecord.objects.filter(Q(fqdn=test) , Q(type='A') | Q(type='AAAA'))
								for x in related:
									dr.dnsrecord.add(x)
							dr.save()
							#Check if this object exists in our model (host, address and type)
							#If we find a host by this FQDN, tie the address to it. Else skip and add address / record.
				except ValueError as e:
				#	#pass
					print 'EXCEPTION ON:' + r + ':' + rtype + ' ;;ValueError; ' + e.message
				except AttributeError as e:
					pass
				except TypeError as e:
					print 'EXCEPTION ON:' + r + ':' + rtype + ' ;;TypeError; ' + e.message
					print traceback.print_tb(sys.exc_info()[2] )
