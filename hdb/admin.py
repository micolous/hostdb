from django.contrib import admin

from models import *

class DNSZoneAdmin(admin.ModelAdmin):
	search_fields = ['zonename']

admin.site.register(DNSZone, DNSZoneAdmin)


class DHCPScopeAdmin(admin.ModelAdmin):
	search_fields = ['zonename']

admin.site.register(DHCPScope, DHCPScopeAdmin)

class HostAdmin(admin.ModelAdmin):
	search_fields = ['zone__zonename', 'hostname', 'User__name', 'location']
	list_display = ['hostname', 'os', 'owner']
	filter_horizontal = [ 'zone' ]

admin.site.register(Host, HostAdmin)

class AddressAdmin(admin.ModelAdmin):
	list_display = ['type', 'host', 'address', 'vlan', 'hwid']
	list_filter = ['type', 'vlan']
	search_fields = ['host__hostname', 'address', 'hwid']
	list_editable = ['address', 'vlan']

admin.site.register(Address, AddressAdmin)

class DHCPHostAdmin(admin.ModelAdmin):
	pass

admin.site.register(DHCPHost, DHCPHostAdmin)

class DNSRecordAdmin(admin.ModelAdmin):
	list_display = ['fqdn', 'type', 'record', 'address','active', 'is_active','zone']
	list_filter = [ 'type', 'zone__zonename' ]
	filter_horizontal = [ 'dnsrecord' ]
	list_editable = ['active'] 

admin.site.register(DNSRecord, DNSRecordAdmin)

class DHCPOptionAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

admin.site.register(DHCPOption, DHCPOptionAdmin)

class DHCPValueAdmin(admin.ModelAdmin):
	list_display = ['scope', 'host', 'option', 'value']

admin.site.register(DHCPValue, DHCPValueAdmin)

