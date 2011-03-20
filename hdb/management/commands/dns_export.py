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
		
	def handle(self, filename, zonename, *args, **options):
		if not filename and if not dirname:
			print "Must supply valid filename or directory name."
			exit(-1)
		if not zonename:
			print "Must supply valid zonename"
			exit(-1)