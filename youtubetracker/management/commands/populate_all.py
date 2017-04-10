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
        fpath = 'http://127.0.0.1:8000/youtubetracker/static/youtubetracker/excel/baseline.xls'
        xl_workbook = xlrd.open_workbook(fpath)
        # Or grab the first sheet by index 
        xl_sheet = xl_workbook.sheet_by_index(0)
        # Pull the first row by index
        
        rowpointer = 0
        allurls = []
        # Can potentially add in requests to get pub date of video below
        for row in range(xl_sheet.nrows):
            row = xl_sheet.row(rowpointer)
            # 0 - Name
            # 1 - Youtube link
            # 2 - Community
            # 3 - Projected
            # 4 - Cost

            marketer = row[0].value
            MYURL = row[1].value
            community = row[2].value
            projected = int(row[3].value)
            cost = int(row[4].value)

            
            page = requests.get(MYURL)
            time.sleep(1.5)
            tree = html.fromstring(page.content)
            views = tree.xpath('//*[@id="watch7-views-info"]/div[1]/text()')
            title = tree.xpath('//*[@id="eow-title"]/text()')
            pubdate = tree.xpath('//*[@id="watch-uploader-info"]/strong/text()')

            try:
                pubdate = pubdate[0].replace('Published on ', '')
                datetimeobject = datetime.datetime.strptime(pubdate, '%b %d, %Y')
                title = title[0].strip()
                views = views[0]
                viewcountint = int(filter(str.isdigit, views))
                if marketer == "Angie" or marketer == "Emily" or marketer == "Jacob" or marketer == "Unknown":
                    language = "English"
                if marketer == "Melissa" or marketer == "Valeria" or marketer == "Mauricio":
                    language = "Spanish"
                if marketer == "Louise" or marketer == "Juliana":
                    language = "Portuguese"
                if marketer == "Sarah" or marketer == "Noor":
                    language = "Arabic"
                if marketer == "Toby":
                    language = "Russian"
            except: 
                print MYURL + " ERROR!!!"
            try:
                video = Video(
                        marketer = marketer,
                        url = MYURL,
                        community = community,
                        cost = cost,
                        publishdate = datetimeobject,
                        language = language,
                        title = title,
                        projectedviews = projected,
                        )
                video.save()
                print marketer, MYURL, community, projected, cost, viewcountint, title, pubdate, datetimeobject, language
            except:
                e = sys.exc_info()[0]
                print e
            rowpointer += 1



        

        

    def handle(self, *args, **options):
        self.populate()

