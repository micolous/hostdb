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
	class Meta:
		verbose_name = 'DNS Zone'
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
	last_exported = DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.zonename
	def clean(self):
		if self.zonename[-1] != '.':
			self.zonename += '.'

class DHCPScope(Model):
	"""
	This represents a DHCP segment, with the first being
	Global, the rest being segments one node down. These
	Fields are all nullable, as they can come from the global zone
	"""
	class Meta:
		verbose_name = 'DHCP Scope'
	#One zone should be called "global" and specify no range
	dnszone = ForeignKey(DNSZone, null=True, blank=True )
	zonename = TextField(max_length=1024, unique=True)
	subnet = CharField(max_length=18, null=True, blank=True, unique=True)
	def __unicode__(self):
		return self.zonename

class Host(Model):
	zone = ManyToManyField( DNSZone, blank=True , null = True)
	owner = ForeignKey(User, null=True, on_delete=SET_NULL)
	hostname = CharField(max_length=255)
	os = CharField(max_length=200)
	description = TextField()
	notes = TextField()
	location = CharField(max_length=255)
	def __unicode__(self):
		zones=self.zone.all()
		if len(zones)==1:
			return u"%s.%s" % (self.hostname, zones[0].zonename)
		elif len(zones)>1:
			return u"%s.{%s}" % (self.hostname, u"".join(z.zonename for z in zones))
		return self.hostname

class Address(Model):
	class Meta:
		verbose_name_plural = 'Addresses'
	IPv4 = 4; IPv6 = 6
	IP_TYPE_CHOICES = (	(IPv4, 'IPv4'), (IPv6, 'IPv6'), )
	host = ForeignKey(Host, null=True, blank=True)
	type = IntegerField(choices=IP_TYPE_CHOICES)
	vlan = IntegerField()
	hwid = CharField(max_length=17, null=True)
	address = CharField(max_length=39, unique=True)
	active = BooleanField(default = True)
	#validate wether it is ipv4 or ipv6
	def __unicode__(self):
		return self.address 
	def clean(self):
		#try:
		#	IP(address)
		#except:
		#	raise ValidationError('Invalid IP address')	
		if type == 4:
			#validate hwid as a mac address
			pass
		else:
			#validate duid
			pass

class DHCPHost(Model):
	class Meta:
		verbose_name = 'DHCP Host'
	address = ForeignKey(Address)
	#Foreign key to a set of DHCP options .... ?
	#Only if this is ipv6
	duid = CharField(max_length=255)

class DNSRecord(Model):
	class Meta:
		verbose_name = 'DNS Record'
	DNS_TYPE_CHOICES = (
		('A', 'A'),
		('AAAA', 'AAAA'),
		('NS', 'NS'),
		('CNAME', 'CNAME'),
		('ACNAME', 'ACNAME'),
		('AAAACNAME', 'AAAACNAME'),
		('DNAME', 'DNAME'),
		('MX', 'MX'),
		('TXT', 'TXT'),
		('HINFO', 'HINFO'),
		('PTR', 'PTR'),
		('SRV', 'SRV')

	)
	address = ForeignKey(Address, null=True, blank=True)
	zone = ForeignKey(DNSZone)
	dnsrecord = ManyToManyField("self", related_name="dnschildren", null=True, blank=True)
	fqdn = CharField(max_length=255, null=True, blank=True)
	type = CharField(max_length=9, choices=DNS_TYPE_CHOICES)
	record = TextField(max_length=1024, null=True, blank=True) #This shouldn't be edited? should it be generated?
	ttl = IntegerField(blank=True, null=True)
	active = BooleanField(default = False)
	modified = DateTimeField(auto_now=True, auto_now_add=True, editable=False)
	#class Admin:
	#	hide_unless = {
	#			'record': {'record' : 'CNAME'}
	#			}
	def __unicode__(self):
		if self.type in ('A', 'AAAA', 'PTR') :
			return u'%s : %s : %s' % (self.fqdn , self.type , self.address)
		if self.type in ('CNAME', 'ACNAME', 'AAAACNAME'):
			return u'%s : %s : %s' % (self.fqdn , self.type , self.dnsrecord)
		return u'%s : %s : %s' % (self.fqdn , self.type , self.record)
	def clean(self):
		if self.type not in ('A', 'AAAA', 'PTR'):
			self.address = None
		if self.type in ('A', 'AAAA', 'CNAME', 'NS', 'PTR', 'ACNAME', 'AAAACNAME'):
			#A records need to record data, since they are Address pointers
			# TODO Should I self generate record entries based on internal information to simplify the export?
			self.record = None
		if self.type == 'A':
			if self.address.type != 4:
				raise ValidationError('IPv6 Address provided for A record')
		if self.type == 'AAAA':
			if self.address.type != 6:
				raise ValidationError('IPv4 Address provided for AAAA record')
		#need to check for records with a _ in them .... 
	def is_active(self, depth=0):
		# This should only send back that it is not active if ALL its parents are False.
		if depth > 100:
			return False
		parent_active = False
		recs = self.dnsrecord.all()
		if depth > 50:
			#We have recursed to far, should I throw an exception?
			return False
		if self.type in ('A', 'AAAA'):
			if self.address.active:
				return self.active
			else:
				return False
		if len(recs) == 0:
			return self.active
		else:
			#we have parents ... Check our self first though .... 
			if self.active == False:
				return False
			# Now, we want to check our parent, since we ARE active, so only our parent can overide this.
			for rec in recs:
				if rec.is_active(depth + 1)==True: 
					return True
			return False
	is_active.boolean = True
	#NOTE fqdn = full name of record 
	# NOTE record = data. 

class DHCPOption(Model):
	class Meta:
		verbose_name = 'DHCP Option'
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
	class Meta:
		verbose_name = 'DHCP Value'
	scope = ForeignKey(DHCPScope, null=True, blank=True)
	host = ForeignKey(DHCPHost, null=True, blank=True)
	option = ForeignKey(DHCPOption)
	value = CharField(max_length=255, null=True, blank=True)
