# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DNSZone.rndckey'
        db.add_column('hdb_dnszone', 'rndckey', self.gf('django.db.models.fields.TextField')(default='a'), keep_default=False)

        # Adding field 'DNSZone.email'
        db.add_column('hdb_dnszone', 'email', self.gf('django.db.models.fields.CharField')(default='2', max_length=255), keep_default=False)

        # Adding field 'DNSZone.serial'
        db.add_column('hdb_dnszone', 'serial', self.gf('django.db.models.fields.IntegerField')(default='2'), keep_default=False)

        # Adding field 'DNSZone.refresh'
        db.add_column('hdb_dnszone', 'refresh', self.gf('django.db.models.fields.IntegerField')(default='2'), keep_default=False)

        # Adding field 'DNSZone.retry'
        db.add_column('hdb_dnszone', 'retry', self.gf('django.db.models.fields.IntegerField')(default='2'), keep_default=False)

        # Adding field 'DNSZone.expire'
        db.add_column('hdb_dnszone', 'expire', self.gf('django.db.models.fields.IntegerField')(default='2'), keep_default=False)

        # Adding field 'DNSZone.minimum'
        db.add_column('hdb_dnszone', 'minimum', self.gf('django.db.models.fields.IntegerField')(default='2'), keep_default=False)

        # Adding field 'DHCPScope.dnszone'
        db.add_column('hdb_dhcpscope', 'dnszone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hdb.DNSZone'], null=True, blank=True), keep_default=False)

        # Adding field 'DHCPScope.subnet'
        db.add_column('hdb_dhcpscope', 'subnet', self.gf('django.db.models.fields.CharField')(max_length=18, unique=True, null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'DHCPScope', fields ['zonename']
        db.create_unique('hdb_dhcpscope', ['zonename'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'DHCPScope', fields ['zonename']
        db.delete_unique('hdb_dhcpscope', ['zonename'])

        # Deleting field 'DNSZone.rndckey'
        db.delete_column('hdb_dnszone', 'rndckey')

        # Deleting field 'DNSZone.email'
        db.delete_column('hdb_dnszone', 'email')

        # Deleting field 'DNSZone.serial'
        db.delete_column('hdb_dnszone', 'serial')

        # Deleting field 'DNSZone.refresh'
        db.delete_column('hdb_dnszone', 'refresh')

        # Deleting field 'DNSZone.retry'
        db.delete_column('hdb_dnszone', 'retry')

        # Deleting field 'DNSZone.expire'
        db.delete_column('hdb_dnszone', 'expire')

        # Deleting field 'DNSZone.minimum'
        db.delete_column('hdb_dnszone', 'minimum')

        # Deleting field 'DHCPScope.dnszone'
        db.delete_column('hdb_dhcpscope', 'dnszone_id')

        # Deleting field 'DHCPScope.subnet'
        db.delete_column('hdb_dhcpscope', 'subnet')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hdb.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.Host']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'vlan': ('django.db.models.fields.IntegerField', [], {})
        },
        'hdb.dhcphost': {
            'Meta': {'object_name': 'DHCPHost'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.Address']"}),
            'duid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'hdb.dhcpoption': {
            'Meta': {'object_name': 'DHCPOption'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'hdb.dhcpscope': {
            'Meta': {'object_name': 'DHCPScope'},
            'dnszone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DNSZone']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subnet': ('django.db.models.fields.CharField', [], {'max_length': '18', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zonename': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '1024'})
        },
        'hdb.dhcpvalue': {
            'Meta': {'object_name': 'DHCPValue'},
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DHCPHost']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DHCPOption']"}),
            'scope': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DHCPScope']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'hdb.dnsrecord': {
            'Meta': {'object_name': 'DNSRecord'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.Address']"}),
            'dnsrecord': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_records'", 'null': 'True', 'to': "orm['hdb.DNSRecord']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DNSZone']"})
        },
        'hdb.dnszone': {
            'Meta': {'object_name': 'DNSZone'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expire': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum': ('django.db.models.fields.IntegerField', [], {}),
            'refresh': ('django.db.models.fields.IntegerField', [], {}),
            'retry': ('django.db.models.fields.IntegerField', [], {}),
            'rndckey': ('django.db.models.fields.TextField', [], {}),
            'serial': ('django.db.models.fields.IntegerField', [], {}),
            'ttl': ('django.db.models.fields.IntegerField', [], {}),
            'zonename': ('django.db.models.fields.TextField', [], {'max_length': '1024'})
        },
        'hdb.host': {
            'Meta': {'object_name': 'Host'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hdb.DNSZone']"})
        }
    }

    complete_apps = ['hdb']
