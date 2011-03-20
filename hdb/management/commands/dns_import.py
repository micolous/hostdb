#from django.conf import settings
#from models import *
#import models
from os import path
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from hostdb.hdb.models import *

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

	def handle(self, filename, zonename, *args, **options):
		if not filename:
			print "Must supply valid filename"
			exit(-1)
		if not zonename:
			print "Must supply valid zonename"
			exit(-1)
		
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
			dnsz = DNSZone.objects.filter(zonename=zonename)[0]
		
		#We want to populate the A and AAAA records first, else we wont have integrity for the other records.
		for rtype in ('A', 'AAAA', 'MX', 'PTR', 'TXT', 'SRV', 'CNAME', 'NS', 'HINFO'):
			for r in z.names:
				try:
					for rec in z.names[r].records(rtype).items:
						if rtype is not 'MX':
							print r + ':' + rtype + ':' + rec
						else:
							print r + ':' + rtype + ':' + rec[0][0] + ' ' + rec[0][1]
						#Check if the record exists or not
						if len(DNSRecord.objects.filter(type=rtype,record=rec,fqdn=r)) == 0:
							dr = DNSRecord()
							dr.zone = dnsz
							dr.type = rtype
							#Make this work for MX records
							dr.record = rec
							dr.ttl = dnsz.ttl
							dr.fqdn = r
							if rtype in ('A', 'AAAA'):
								if len(Address.objects.filter(address=rec)) == 0:
									#Then we need to create it.
									a = Address()
									a.host = None
									a.type = 6
									if rtype == 'A':
										a.type = 4
									a.vlan = 0
									a.mac = None
									a.address = rec
								else:
									a.save()
									dr.address = a
							if rtype in ('MX', 'CNAME', 'NS'):
								related = DNSRecord.objects.filter(Q(fqdn=r) , Q(type='A') | Q(type='AAAA'))
								if len(related) == 0:
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
			
