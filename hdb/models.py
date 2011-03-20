from django.db.models import *
from django.contrib.auth.models import User
from IPy import IP
from django.core.exceptions import ValidationError

# Create your models here.
#not null by default

class DNSZone(Model):
	"""
	This is a DNS zone, and represents both a view in named.conf
	But also a zone file that is generated from related addresses
	"""
	zonename = TextField(max_length=1024, unique=True)
	#ACL's
	#Permissions
	ttl = IntegerField()
	rndckey = TextField()
	#fk email to a user?
	email = CharField(max_length=255)
	serial = IntegerField()
	refresh = IntegerField()
	retry = IntegerField()
	expire = IntegerField()
	minimum = IntegerField()
	def __unicode__(self):
		return self.zonename

class DHCPScope(Model):
	"""
	This represents a DHCP segment, with the first being
	Global, the rest being segments one node down. These
	Fields are all nullable, as they can come from the global zone
	"""
	#One zone should be called "global" and specify no range
	dnszone = ForeignKey(DNSZone, null=True, blank=True )
	zonename = TextField(max_length=1024, unique=True)
	subnet = CharField(max_length=18, null=True, blank=True, unique=True)
	def __unicode__(self):
		return self.zonename

class Host(Model):
	zone = ForeignKey(DNSZone)
	owner = ForeignKey(User)
	hostname = CharField(max_length=255)
	os = CharField(max_length=200)
	description = TextField()
	notes = TextField()
	location = CharField(max_length=255)
	def __unicode__(self):
		return self.hostname + '.' + self.zone.zonename

class Address(Model):
	IPv4 = 4; IPv6 = 6
	IP_TYPE_CHOICES = (	(IPv4, 'IPv4'), (IPv6, 'IPv6'), )
	host = ForeignKey(Host, null=True, blank=True)
	type = IntegerField(choices=IP_TYPE_CHOICES)
	vlan = IntegerField()
	mac = CharField(max_length=17, null=True)
	address = CharField(max_length=39, unique=True)
	#validate wether it is ipv4 or ipv6
	def __unicode__(self):
		return self.address 
	def clean(self):
		#try:
		#	IP(address)
		#except:
		#	raise ValidationError('Invalid IP address')	
		pass	

class DHCPHost(Model):
	address = ForeignKey(Address)
	#Foreign key to a set of DHCP options .... ?
	#Only if this is ipv6
	duid = CharField(max_length=255)

class DNSRecord(Model):
	DNS_TYPE_CHOICES = (
		('A', 'A'),
		('AAAA', 'AAAA'),
		('NS', 'NS'),
		('CNAME', 'CNAME'),
		('MX', 'MX'),
		('TXT', 'TXT'),
		('HINFO', 'HINFO'),
		('PTR', 'PTR'),
		('SRV', 'SRV')

	)
	address = ForeignKey(Address, null=True, blank=True)
	zone = ForeignKey(DNSZone)
	dnsrecord = ManyToManyField("self", null=True, blank=True)
	fqdn = CharField(max_length=255, null=True, blank=True)
	type = CharField(max_length=5, choices=DNS_TYPE_CHOICES)
	record = TextField(max_length=1024) #This shouldn't be edited? should it be generated?
	ttl = IntegerField(blank=True, null=True)
	def __unicode__(self):
		return self.type + ' : ' + self.record
	def clean(self):
		pass
	

class DHCPOption(Model):
	"""
	This is a list of options that can be applied to DHCP object
	These should not be things like hardware-ethernet address
	or the ip address allocated, these are derived from the DHCPhost
	Things like router, gateway, bootfile .... 
	"""
	name = CharField(max_length=255)
	code = CharField(max_length=255, unique=True)
	def __unicode__(self):
		return self.name

class DHCPValue(Model):
	scope = ForeignKey(DHCPScope, null=True, blank=True)
	host = ForeignKey(DHCPHost, null=True, blank=True)
	option = ForeignKey(DHCPOption)
	value = CharField(max_length=255, null=True, blank=True)
