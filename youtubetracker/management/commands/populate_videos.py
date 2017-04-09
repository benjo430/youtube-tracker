from django.core.management.base import BaseCommand
from youtubetracker.models import Video, Viewcount
import requests
from lxml import html
import time
import datetime
import csv
import xlrd
import sys

class Command(BaseCommand):
	# This class allows us to run database populating commands by typing "python manage.py populate_db" into terminal
	# Read here for more info: http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
	# turn into two scripts (separate files) one to populate database from a spreadsheet and another to update all entries in database to add view counts for the day.
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def populate(self):
        # Open the workbook
        fpath = '/Users/benjaminanderson/Dropbox/Programming/djangotutorial/djangoproject/mysite/youtubetracker/management/commands/test.xls'
        xl_workbook = xlrd.open_workbook(fpath)
        # Or grab the first sheet by index 
        xl_sheet = xl_workbook.sheet_by_index(0)
        # Pull the first row by index
        
        rowpointer = 0
        # Can potentially add in requests to get pub date of video below
        for row in range(xl_sheet.nrows):
            row = xl_sheet.row(rowpointer)
            # Hard coded info:
            # 0 = URL
            # 1 = Marketer
            # 2 = Community
            # 3 = Cost
            URL = row[0].value
            marketer = row[1].value
            community = row[2].value
            cost = row[3].value
            try:
                print URL
                video = Video(marketer=marketer,url=URL,community=community,cost=cost, publishdate=datetime.date.today())
                video.save()

            except:
                e = sys.exc_info()[0]
                print e
            rowpointer += 1



        

        

    def handle(self, *args, **options):
        self.populate()

