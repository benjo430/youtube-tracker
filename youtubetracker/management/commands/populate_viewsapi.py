from django.core.management.base import BaseCommand
from youtubetracker.models import Video, Viewcount
import requests
from lxml import html
import time
import datetime
import urlparse
import json

class Command(BaseCommand):
	# This class allows us to run database populating commands by typing "python manage.py populate_db" into terminal
	# Read here for more info: http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
	# turn into two scripts (separate files) one to populate database from a spreadsheet and another to update all entries in database to add view counts for the day.
    args = '<foo bar ...>'
    help = 'our help string comes here'
    #"https://www.googleapis.com/youtube/v3/videos?id=YLzTFYYDnnk&key=AIzaSyAveZmaAE0CHPPt6dSY4o_oitb-QTKp9ZU%20&part=snippet,statistics"
    # Broken Vid: https://www.youtube.com/watch?v=ytZW3iyoFho

    def populate(self):
        # video = Video(marketer="Jacob",url="https://www.youtube.com/watch?v=68cQp8ysiNc",community="Minecraft",cost="14424")
        # video.save()
        allvideos = Video.objects.all()
        print "Populating View Count for all videos in database..."
        for video in allvideos:
            # Get ID from Youtube URL
            query = urlparse.urlparse(video.url)
            if query.hostname == 'youtu.be':
                videoid = query.path[1:]
            if query.hostname in ('www.youtube.com', 'youtube.com'):
                if query.path == '/watch':
                    p = urlparse.parse_qs(query.query)
                    videoid = p['v'][0]
                if query.path[:7] == '/embed/':
                    videoid = query.path.split('/')[2]
                if query.path[:3] == '/v/':
                    videoid = query.path.split('/')[2]
            # fail?
            else:
                videoid =""

            today = datetime.date.today()
            # print videoid, video.url

            # Most recently added view count for this video. Use this to check 
            # if it view count was already updated for today.
            #mostrecentdate = video.viewcount_set.order_by('-id')[0].viewcountdate
            mostrecentdate = video.viewcount_set.order_by('-id')
            empty = False
            if not mostrecentdate:
                #print "NOTHING HERE"
                empty = True

            else:
                mostrecentdate = mostrecentdate[0].viewcountdate
                #print mostrecentdate
            if mostrecentdate != today or empty == True:
                # Use requests to get the view count from the URL in the database.
                try:
                    page = requests.get("https://www.googleapis.com/youtube/v3/videos?id=" + videoid + "&key=AIzaSyAveZmaAE0CHPPt6dSY4o_oitb-QTKp9ZU%20&part=snippet,statistics")
                    json_data = json.loads(page.text)
                    #print video.url
                    viewcountint = json_data['items'][0]['statistics']['viewCount']
                except KeyError:
                    print "KEY ERROR TRYING SCRAPING"
                    try:
                        page = requests.get(video.url)
                    except requests.exceptions.ConnectionError:
                        r.status_code = "Connection refused"
                    time.sleep(10)
                    tree = html.fromstring(page.content)
                    views = tree.xpath('//*[@id="watch7-views-info"]/div[1]/text()')

                    try:
                        str1 = views[0]
                    except: 
                        #print video.url + " ERROR!!!"
                        pass
                    viewcountint = int(filter(str.isdigit, str1))
                print viewcountint
                
                try:
                    q = Video.objects.get(url=video.url)
                    q.viewcount_set.create(viewcountdate=today,viewcount=viewcountint)
                except:
                    print "Already added view count" + video.url


            #     try:
            #         str1 = views[0]
            #     except:	
            #         print video.url + " ERROR!!!"
            #     viewcountint = int(filter(str.isdigit, str1))
            #     print viewcountint
                
            #     q = Video.objects.get(url=video.url)
            #     q.viewcount_set.create(viewcountdate=today,viewcount=viewcountint)
            # else:
            #     print "Already added view count for today for " + video.url
        
        # Used for testing:
        # q = Video.objects.get(pk=13)
        # q.viewcount_set.create(viewcountdate="2009-10-04",viewcount="32142")

        

    def handle(self, *args, **options):
        self.populate()