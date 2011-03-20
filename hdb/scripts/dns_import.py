#from django.conf import settings
#from models import *
#import models
from hostdb.hdb.models import *

from easyzone import easyzone
from easyzone.zone_check import ZoneCheck
#read the user input, to determine the zone name, and file to be read.

filename = '/Users/williambrown/development/firstyear.id.au.zone'
zname = 'firstyear.id.au'

c = ZoneCheck(checkzone='/usr/sbin/named-checkzone')

if not c.isValid(zname, filename):
	print "Invalid zone"
	quit()

z = easyzone.zone_from_file(zname, filename)

if len(DNSZone.objects.filter(zonename=zname)) is 0:
	dnsz = DNSZone()
	dnsz.zonename = zname
	dnsz.ttl = z.root.soa.minttl
	dnsz.rndckey = '/etc/named/rndc.key'
	#fk email to a user?
	dnsz.email = 'william.e.brown@adelaide.edu.au'
	dnsz.serial = z.root.soa.serial
	dnsz.refresh = z.root.soa.refresh
	dnsz.retry = z.root.soa.retry
	dnsz.expire = z.root.soa.expire
	dnsz.minimum = z.root.soa.minttl
	dnsz.save()
else:
	dnsz = DNSZone.objects.filter(zonename=zname)[0]

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
				if len(DNSRecord.objects.filter(type=rtype,record=rec,fqdn=r)) is 0:
					dr = DNSRecord()
					dr.zone = dnsz
					dr.type = rtype
					#Make this work for MX records
					dr.record = rec
					dr.ttl = dnsz.ttl
					dr.fqdn = r
					if rtype is 'A' or rtype is 'AAAA':
						if len(Address.objects.filter(address=rec)) is 0:
							#Then we need to create it.
							a = Address()
							a.host = None
							a.type = 6
							if rtype is 'A':
								a.type = 4
							a.vlan = 0
							a.mac = None
							a.address = rec
							a.save()
							dr.address = a
					if rtype is 'MX' or rtype is 'CNAME' or rtype is 'NS':
						related = DNSRecord.objects.filter(Q(fqdn=r) , Q(type='A') | Q(type='AAAA'))
						if len(related) is not 0:
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
			
