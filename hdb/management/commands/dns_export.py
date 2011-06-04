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
		
		#We get our list of DNSRecord objects, all if there is no zonename specified
		if zonename:
			dnsz_list = DNSZone.objects.filter(zonename=zonename)
		else:
			dnsz_list = dnsz = DNSZone.objects.all()
		for dnsz in dnsz_list:
			#This could be made to the datestamp
			#TODO zonename needs to be set here ... 
			dnsz.serial = datetime.datetime.now().strftime("%Y%m%d%H%M")
			dnsz.save()
			for nsserver in dnsz.dnsrecord_set.filter(type="NS"):
				self.exportZone("%s.%s.zone" %(nsserver.fqdn, zonename ) , dnsz, nsserver, zonename)
		
	def exportZone(self, filename, dnsz, nsserver, zonename):
		#Create or edit the file. Put the SOA details in.
		# Fill in the template. 
		#do we need to touch this first.
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
			for arecord in dnsz.dnsrecord_set.filter( record=zonename, type__in=( 'A', 'AAAA' ) ):
				f.write('	%s %s \n' % (arecord.type, arecord.address) )
		#f.close()
		z = easyzone.zone_from_file(dnsz.zonename, filename)
		#z.root.soa.minttl = dnsz.ttl
		#dnsz.rndckey = keyfile
		#fk email to a user?
		#dnsz.email = 'william.e.brown@adelaide.edu.au'
		#z.root.soa.refresh = dnsz.refresh
		#z.root.soa.retry = dnsz.retry
		#z.root.soa.expire = dnsz.expire
		#z.root.soa.minttl = dnsz.minimum
		#Serial number - take date or serial + 1, which ever is larger. Save this back to the dnsz.
		#dnsz.serial += 1
		#dnsz.save()
		#z.root.soa.serial = dnsz.serial 
		
		#Take all the records in the dnsz, sort alphabetically. This helpfully, creates our A records first
		z.save(autoserial=False)
		
