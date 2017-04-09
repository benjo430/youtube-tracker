from django.core.management.base import BaseCommand
from youtubetracker.models import Video, Viewcount
import requests
from lxml import html
import time
import datetime

class Command(BaseCommand):
	# This class allows us to run database populating commands by typing "python manage.py populate_db" into terminal
	# Read here for more info: http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
	# turn into two scripts (separate files) one to populate database from a spreadsheet and another to update all entries in database to add view counts for the day.
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def populate(self):
        # video = Video(marketer="Jacob",url="https://www.youtube.com/watch?v=68cQp8ysiNc",community="Minecraft",cost="14424")
        # video.save()

        allvideos = Video.objects.all()

        for video in allvideos:
        	print "Populating View Count for all videos in database..."
        	print video.url

        	# Use requests to get the view count from the URL in the database.
        	page = requests.get(video.url)
        	time.sleep(1.5)
        	tree = html.fromstring(page.content)
        	views = tree.xpath('//*[@id="watch7-views-info"]/div[1]/text()')
        
        	try:
        		str1 = views[0]
        	except:	
        		print video.url + " ERROR!!!"
    		viewcountint = int(filter(str.isdigit, str1))
    		print viewcountint
    		today = datetime.date.today()
    		q = Video.objects.get(url=video.url)
    		q.viewcount_set.create(viewcountdate=today,viewcount=viewcountint)

        # q = Video.objects.get(pk=3)
        # q.viewcount_set.create(viewcountdate="2009-10-04",viewcount="32142")

        

    def handle(self, *args, **options):
        self.populate()