import urlparse
import requests
import json
import time
from lxml import html
from .models import Video, Viewcount
import datetime
from datetime import timedelta
from datetime import date
import json
import time

def populate():
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

           
def get_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

# print get_video_id("https://youtu.be/i2ZeaD6gA_A")


def tryapi(videoid):
    # Use requests to get the view count from the URL in the database.
    try:
        makeurl = "https://www.googleapis.com/youtube/v3/videos?id=" + videoid + "&key=AIzaSyAveZmaAE0CHPPt6dSY4o_oitb-QTKp9ZU%20&part=snippet,statistics"
        page = requests.get(makeurl)

    except:
        print "Unable to Load with API: ", "https://www.youtube.com/watch?v="+videoid
        return False
    try:
        json_data = json.loads(page.text)
        viewcountint = json_data['items'][0]['statistics']['viewCount']
    except:
        print "Wasn't able to get JSON data: ", "https://www.youtube.com/watch?v="+videoid
        return False

    return viewcountint
    
def tryscrape(videoid):
    createurl = "https://www.youtube.com/watch?v="+videoid
    print createurl
    try:
        page = requests.get(createurl)
        time.sleep(1)
        tree = html.fromstring(page.content)
        views = tree.xpath('//*[@id="watch7-views-info"]/div[1]/text()')
        
    except:
        print "Couldn't request link during try scrape"
        return False
    try:
        str1 = views[0]
        viewcountint = int(filter(str.isdigit, str1))
    except:
        return False
        print "Wasn't able to get data needed from scrapping"
    return viewcountint
            