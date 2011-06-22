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
import os
#read the user input, to determine the zone name, and file to be read.

#filename = 'firstyear.id.au.zone'
#zname = 'firstyear.id.au'

class Command(BaseCommand):
	can_import_settings = True
	help = "Import dns zone file to database and bring it under hdb control."
	option_list = BaseCommand.option_list + (
		#make_option('-f', '--file',
		#	dest='filename',
		#	metavar = 'FILE',
		#	default = None,
		#	help='dns zone file to export to. If not specified, will default to "zonename.zone" '),
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
		make_option('-f', '--force',
			action='store_true',
			dest='force_write',
			default=False,
			help='force writing of zone files even if no updates are needed',),
		
		make_option('-n', '--nameserver',
			dest='nameserver',
			metavar = 'NAMESERVER',
			default = None,
			help='specify the nameserver you wish to export zones for. If not specified, export zones to all nameservers.'),
		)
		
	def handle(self, zonename, dirname, checkzone, verbosity, force_write, nameserver, *args, **options):
		if not zonename and not dirname:
			print "Must supply valid zonename. If you wish to export all zones, provide a dirname"
			exit(-1)
		#if not filename and if not dirname:
		#	print "Must supply valid filename or directory name."
		#	exit(-1)
		if not dirname:
			dirname = './'
		if dirname[-1] != '/':
			dirname += '/'
		if (verbosity > '1'):
			print 'zonename: %s' % zonename
			print 'dirname: %s' % dirname
			print 'checkzone: %s' % checkzone
			print 'force_write: %s' % force_write
		#We get our list of DNSRecord objects, all if there is no zonename specified
		if zonename:
			if zonename[-1] != '.':
				zonename += '.'
			dnsz_list = DNSZone.objects.filter(zonename=zonename)
		else:
			dnsz_list = dnsz = DNSZone.objects.all()
		if verbosity > '1':
			print dnsz_list
		for dnsz in dnsz_list:
			#This could be made to the datestamp
			#TODO zonename needs to be set here ... 
			#dnsz.serial = datetime.datetime.now().strftime("%Y%m%d%H")
			dnsz.serial += 1
			dnsz.save()
			if nameserver == None:
				nsservers = dnsz.dnsrecord_set.filter(type="NS")
			else:
				nsservers = []
				# There is probably a better way to do this .... 
				nsservers_ = dnsz.dnsrecord_set.filter(type="NS")
				for nsserver_ in nsservers_:
					if len(nsserver_.dnsrecord.filter(fqdn=nameserver)) > 0:
						if verbosity > '0':
							print len(nsserver_.dnsrecord.filter(fqdn=nameserver))
							print nsserver_
						nsservers.append( nsserver_)
			for nsserver in nsservers:
				filename = "%s%s%szone" %(dirname, nsserver.record, dnsz.zonename )
				filename_tmp = filename + '.tmp'
				if verbosity > '1':
					print 'filename: %s' % filename
					print 'filename_tmp: %s' % filename_tmp
				exported = self.exportZone(filename_tmp , dnsz, nsserver, dnsz.zonename, force_write, verbosity)
				if verbosity > '1':
					print 'exported: %s' % exported
				#now we need to check the zone
				if exported:
					check = ZoneCheck(checkzone=checkzone)
					res = check.isValid(dnsz.zonename, filename_tmp  )
					if verbosity > '1':
						print 'check result: %s' % res
					if res:
						#zone is valid, move it into place
						os.rename(filename_tmp, filename)
					else:
						print 'ERROR: invalid zone %s' % dnsz.zonename
						print 'This is either a broken zone, or bad path to checkzone'
						print 'Please check the zone at %s' % filename_tmp
			dnsz.last_exported = datetime.datetime.now()
			dnsz.save()

		
	def exportZone(self, filename, dnsz, nsserver, zonename, write, verbosity):
		if (verbosity > '1'):
			print '-> filename: %s' % filename
			print '-> zonename: %s' % zonename
			print '-> write: %s' % write
			print '-> verbosity: %s' % verbosity
		# TODO: This needs to write to a temp file, check it then if it passes, put it into place.
		# Check our list of zone entries if anything has been updated since the last writeout .... 
		for record in dnsz.dnsrecord_set.all():
			if verbosity > '1':
					print record
					print dnsz.last_exported
					print record.modified
			if dnsz.last_exported < record.modified:
				if verbosity > '1':
					print 'modified'
				write = True
				break
		# We write this time out just for record keepings sake
		if write == False:
			return False
		# Create or edit the file. Put the SOA details in.
		# Fill in the template. 
		# do we need to touch this first
		with open(filename,'w') as f:
			values = model_to_dict(dnsz)
			values ['nsserver'] = nsserver.record
			values ['email'] = values['email'].replace('@','.')
			values ['exporttime'] = datetime.datetime.now().strftime("%Y%m%d%H%M")
			#values ['email'] #Now we need to escape the email
			SOA = ("""$ORIGIN .
			$TTL %(ttl)s
			; This file auto generated by HDB. DO NOT EDIT IT BY HAND.
			; Last export - %(exporttime)s
			%(zonename)s IN SOA %(nsserver)s %(email)s (
				%(serial)s ;serial
				%(refresh)s ; refresh
				%(retry)s ; retry
				%(expire)s ; expire
				%(minimum)s ; minimum
			)
			\n""" % values ).replace("\n\t\t\t", "\n")
			f.write(SOA)
			if verbosity > '1': print SOA
			for nsserver in dnsz.dnsrecord_set.filter( type="NS"):
				if nsserver.is_active():
					f.write('	NS %s \n' %( nsserver.record) )
			for arecord in dnsz.dnsrecord_set.filter( fqdn=zonename, type__in=( 'A', 'AAAA' )):
				if arecord.is_active():
					f.write('	%s %s \n' % (arecord.type, arecord.address) )
			query1 = dnsz.dnsrecord_set.filter( fqdn=zonename)
			query2 = query1.exclude( type__in=('A', 'AAAA', 'NS'))
			for arecord in query2:
				if arecord.is_active():
					f.write('	%s %s \n' % (arecord.type, arecord.record) )
			#Now we write the origin and TTL out ... 
			lttl = values['ttl']
			origin = '.'
			lorigin = '.'
			# For everything NOT with a name of zonename
			for record in dnsz.dnsrecord_set.filter( ~Q(fqdn__exact = zonename) , ~Q(type__exact = 'DNAME') ).order_by('fqdn','type' ) :
				if verbosity > '1': print record
				if record.is_active():
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
					if lttl != record.ttl:
						if record.ttl != None:
							f.write('$TTL %s\n' % record.ttl)
							lttl = record.ttl
					if record.type == 'ACNAME' or record.type == 'AAAACNAME':
						f.write( "%-20s " % (record.fqdn.replace('.' + origin, '') ) )
						for parent_rec in record.dnsrecord.filter(type=record.type.replace('CNAME', '') ):
							f.write ("\t%-10s %s\n" % ( parent_rec.type, parent_rec.record) )
					elif record.type == 'A':
						if record.address.type == 4:
							f.write( "%-20s %-10s %s\n" %( record.fqdn.replace('.'+ origin,'' ) , record.type, record.address.address )  )
						else:
							print 'Invalid address %s for record type %s' % (record.address, record.type)
					elif record.type == 'AAAA':
						if record.address.type == 6:
							f.write( "%-20s %-10s %s\n" %( record.fqdn.replace('.'+ origin,'' ) , record.type, record.address.address )  )
						else:
							print 'Invalid address %s for record type %s' % (record.address, record.type)
					elif record.type == 'CNAME':
						# We want to print our parent records fqdn 
						f.write( "%-20s %-10s %s\n" %( record.fqdn.replace('.'+ origin,'' ) , record.type, record.dnsrecord.all()[0].fqdn )  )
					else:
						f.write( "%-20s %-10s %s\n" %( record.fqdn.replace('.'+ origin,'' ) , record.type, record.record )  )
			# We export DNAME's last else it breaks zone files .... Mind you, DNAME's can break enough as is.
			#WE need to be verbose with DNAME's, so we set our $ORIGIN to ., and work from there.
			dname_records =  dnsz.dnsrecord_set.filter( Q(type__exact = 'DNAME' ) ).order_by('fqdn' ) 
			if len(dname_records) > 0:
				f.write( '$ORIGIN %s\n' % '.' )
				for record in dname_records:
					if verbosity > '1':
						print record
					if lttl != record.ttl:
						if record.ttl != None:
							f.write('$TTL %s\n' % record.ttl)
							lttl = record.ttl
					f.write( "%-20s %-10s %s\n" %( record.fqdn , record.type, record.record )  )
		return True
		
