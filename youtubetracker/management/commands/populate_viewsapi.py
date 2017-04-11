from django.core.management.base import BaseCommand
from youtubetracker.models import Video, Viewcount
import requests
from lxml import html
import time
import datetime
import urlparse
import json
from parse import *
from datetime import timedelta

class Command(BaseCommand):
	# This class allows us to run database populating commands by typing "python manage.py populate_db" into terminal
	# Read here for more info: http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
	# turn into two scripts (separate files) one to populate database from a spreadsheet and another to update all entries in database to add view counts for the day.
    args = '<foo bar ...>'
    help = 'our help string comes here'
    #"https://www.googleapis.com/youtube/v3/videos?id=YLzTFYYDnnk&key=AIzaSyAveZmaAE0CHPPt6dSY4o_oitb-QTKp9ZU%20&part=snippet,statistics"
    # Broken Vid: https://www.youtube.com/watch?v=ytZW3iyoFho


    def populate(self):


        allvideos = Video.objects.all()
        print "Populating View Count for all videos in database..."
           
        for video in allvideos:
            if get_video_id(video.url) is not None:
                videoid = get_video_id(video.url)
    
            # Grab all viewcounts for this video and check the date to ensure its not today.
            mostrecentdate = video.viewcount_set.order_by('-id')
            empty = False
            today = datetime.date.today()
            if not mostrecentdate:
                empty = True
            else:
                mostrecentdate = mostrecentdate[0].viewcountdate


            if mostrecentdate != today or empty == True:
                apiattempt = tryapi(videoid)
                if apiattempt != False:
                    viewcountint = apiattempt
                else:
                    scrapeattempt = tryscrape(videoid)
                    if scrapeattempt != False:
                        viewcountint = scrapeattempt
                    else:
                        print "!!!!!! -------- OUT OF OPTIONS. SETTING TO 0"
                        viewcountint = 0
            try:
                q = Video.objects.get(url=video.url)
                q.viewcount_set.create(viewcountdate=today,viewcount=viewcountint)
                print "SUCCESSFULLY SAVED!"
            except:
               print "Already added view count" + video.url
    
                # try:
                #     q = Video.objects.get(url=video.url)
                #     q.viewcount_set.create(viewcountdate=today,viewcount=viewcountint)
                # except:
                #    print "Already added view count" + video.url


        

    def handle(self, *args, **options):
        self.populate()