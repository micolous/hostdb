#from django.conf import settings
#from models import *
#import models
from os import path
from django.core.management.base import BaseCommand, CommandError
from django.forms.models import model_to_dict
from django.db.models import Q

from optparse import make_option
from hostdb.hdb.models import *

from easyzone import easyzone
from easyzone.zone_check import ZoneCheck
import datetime
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
			help='dns zone file to export to. If not specified, will default to "zonename.zone" '),
		make_option('-z', '--zonename',
			dest='zonename',
			metavar = 'ZONE',
			default = None,
			help='specify the zone you wish to export. If not specified, export all zones to files.'),
		make_option('-d', '--dir',
			dest='dirname',
			metavar = 'DIR',
			default = None,
			help='dns zone file directory to export to. Required when -z is not listed.'),
		make_option('-c', '--checkzone',
			dest='checkzone',
			metavar = 'CHECK',
			default = '/usr/sbin/named-checkzone',
			help='specify the path to the ISC-BIND named-checkzone binary'),
		
		)
		
	def handle(self, filename, zonename, dirname, checkzone, *args, **options):
		if not zonename and not dirname:
			print "Must supply valid zonename. If you wish to export all zones, provide a dirname"
			exit(-1)
		#if not filename and if not dirname:
		#	print "Must supply valid filename or directory name."
		#	exit(-1)
		if zonename[-1] != '.':
			zonename += '.'
		#We get our list of DNSRecord objects, all if there is no zonename specified
		if zonename:
			dnsz_list = DNSZone.objects.filter(zonename=zonename)
		else:
			dnsz_list = dnsz = DNSZone.objects.all()
		for dnsz in dnsz_list:
			#This could be made to the datestamp
			#TODO zonename needs to be set here ... 
			dnsz.serial = datetime.datetime.now().strftime("%Y%m%d%H")
			dnsz.save()
			for nsserver in dnsz.dnsrecord_set.filter(type="NS"):
				self.exportZone("%s.%s.zone" %(nsserver.record, zonename ) , dnsz, nsserver, zonename)
		
	def exportZone(self, filename, dnsz, nsserver, zonename):
		#Create or edit the file. Put the SOA details in.
		# Fill in the template. 
		#do we need to touch this first
		with open(filename,'w') as f:
			values = model_to_dict(dnsz)
			values ['nsserver'] = nsserver.record
			values ['email'] = values['email'].replace('@','.')
			#values ['email'] #Now we need to escape the email
			SOA = ("""$ORIGIN .
			$TTL %(ttl)s
			%(zonename)s IN SOA %(nsserver)s %(email)s (
				%(serial)s ;serial
				%(refresh)s ; refresh
				%(retry)s ; retry
				%(expire)s ; expire
				%(minimum)s ; minimum
			)
			\n""" % values ).replace("\n\t\t\t", "\n")
			f.write(SOA)
			for nsserver in dnsz.dnsrecord_set.filter( type="NS"):
				f.write('	NS %s \n' %( nsserver.record) )
			for arecord in dnsz.dnsrecord_set.filter( fqdn=zonename, type__in=( 'A', 'AAAA' ) ):
				f.write('	%s %s \n' % (arecord.type, arecord.address) )
			#Now we write the origin out ... 
			f.write("$ORIGIN %s\n" % zonename )
			lorigin = zonename
			origin = zonename
			for record in dnsz.dnsrecord_set.filter( ~Q(fqdn__exact = zonename) ).order_by('type') :
				#print record.fqdn + ':' + record.record + ':' + record.type
				pqdn = record.fqdn.replace('.' + zonename, '')
				lorigin = origin
				if '.' in pqdn:
					origin = pqdn.split('.',1)[1] + '.' + zonename
				else: 
					origin = zonename
					#f.write('$ORIGIN %s\n' % zonename)
				if lorigin != origin:
					f.write('$ORIGIN %s\n' % (origin))
				f.write( "%-20s %-5s %s\n" %( record.fqdn.replace('.'+ origin,'' ) , record.type, record.record )  )
		#z = easyzone.zone_from_file(zonename, filename)
		#z.save(autoserial=False)
		
