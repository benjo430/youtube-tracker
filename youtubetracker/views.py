from django.shortcuts import get_object_or_404, render
# from dataextract import *
# Create your views here.
from django.http import HttpResponse
from .models import Video, Viewcount
import datetime
from datetime import timedelta
from datetime import date
import json
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from graphos.sources.simple import SimpleDataSource
# from graphos.renderers.gchart import LineChart

def index(request, date1=False, date2=False, pubdate1=False, pubdate2=False):
	# Get all the youtube videos in the database
	allvideolist = Video.objects.all()
	page = request.GET.get('page',1)

	paginator = Paginator(allvideolist, 30)
	try:
		videolist = paginator.page(page)
	except PageNotAnInteger:
		videolist = paginator.page(1)
	except EmptyPage:
		videolist = paginator.page(paginator.num_pages)


	# Get a clean list of the marketers by name
	videomarketerlist = []
	for marketers in Video.MARKETER:
		videomarketerlist.append(marketers[0])

	# Check if there is a date in the URL
	# If there isn't use default number
	# If there is call getdata function to get data for the date period
	if date1==False:
		# Date is not in URL
		num_days = 25
		
		date1 = (datetime.date.today() - timedelta(num_days)).strftime('%Y-%m-%d')
		date2 = datetime.date.today().strftime('%Y-%m-%d')

		plotdates = getdata(allvideolist,date1,date2,pubdate1,pubdate2)[0]
		plotvalues = getdata(allvideolist,date1,date2,pubdate1,pubdate2)[1]

		

	else:
		# Date is in URL
		plotdates = getdata(allvideolist,date1,date2,pubdate1,pubdate2)[0]
		plotvalues = getdata(allvideolist,date1,date2,pubdate1,pubdate2)[1]

	for i in plotdates:
			print str(i)

	context = {'allvideolist': allvideolist, 'videomarketerlist': videomarketerlist, 'plotdates': plotdates, 'plotvalues': plotvalues, 'videolist': videolist}
	return render(request, 'youtubetracker/index.html', context)


def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'youtubetracker/detail.html', {'video': video})


def marketerdetail(request, marketer_id, date1=False, date2=False, pubdate1=False, pubdate2=False):
	allmarketerlist = Video.objects.all().filter(marketer=marketer_id)
	# Set how far back you want to go date wise. For each date between then and now, 
	# search each item in database for a viewcount matching that date.
	
	# Check if there is a date in the URL
	# If there isn't use default number
	# If there is call getdata function to get data for the date period
	if date1==False:
		# Date is not in URL
		num_days = 25
		
		date1 = (datetime.date.today() - timedelta(num_days)).strftime('%Y-%m-%d')
		date2 = datetime.date.today().strftime('%Y-%m-%d')

		plotdates = getdata(allmarketerlist,date1,date2,pubdate1,pubdate2)[0]
		plotvalues = getdata(allmarketerlist,date1,date2,pubdate1,pubdate2)[1]

	else:
		# Date is in URL
		plotdates = getdata(allmarketerlist,date1,date2,pubdate1,pubdate2)[0]
		plotvalues = getdata(allmarketerlist,date1,date2,pubdate1,pubdate2)[1]


	return render(request, 'youtubetracker/marketerdetail.html', {'marketer_id': marketer_id, 'allmarketerlist': allmarketerlist, 'plotdates': plotdates, 'plotvalues': plotvalues})


# def alldate(request, date1, date2, pubdate1=False, pubdate2=False):
# 	allvideolist = Video.objects.all()

# 	plotdates = getdata(allvideolist,date1,date2)[0]
# 	plotvalues = getdata(allvideolist,date1,date2)[1]
# 	for i in plotvalues:
# 		print i

# 	return render(request, 'youtubetracker/datedetail.html', {'video': date2, 'plotdates': plotdates, 'plotvalues': plotvalues})



def getdata(allobject,date1,date2,pubdate1=False, pubdate2=False):
	# Take an object that contains all the videos and return a tuple with two lists.
	# One contains the plot dates, the other the plot values

	
	plotdates = []
	plotvalues = []
	# Create datetimes out of dates from URL - convert the - to ,
	startingdatetime = datetime.datetime.strptime(date1, '%Y-%m-%d').date() 
	#startingdatetime = datetime.datetime(date1.replace("-",","))
	endingdatetime = datetime.datetime.strptime(date2, '%Y-%m-%d').date()

	startpubdatetime = datetime.datetime.strptime(pubdate1, '%Y-%m-%d').date() 
	endpubdatetime = datetime.datetime.strptime(pubdate2, '%Y-%m-%d').date()


	dayspread = (endingdatetime - startingdatetime).days
	cursor = dayspread

	pubdatedelta = endpubdatetime - startpubdatetime
	listofpublishdates = []
	# populate listofpublishdates list by looking at all the dates between start and end pubdates
	for pubdate in range(pubdatedelta.days + 1):
		listofpublishdates.append(startpubdatetime + timedelta(days=pubdate))

	
	for i in range(dayspread+1):
		extract_date = endingdatetime - timedelta(cursor)
		#print type(extract_date)
		#print "Date: " + str(extract_date)
		viewcountsum = 0
		for video in allobject:
			# Get the all the view counts of this video
			viewcounts = Viewcount.objects.all().filter(video=video)
			for counts in viewcounts:
				if counts.viewcountdate == extract_date and video.publishdate in listofpublishdates:
					viewcountsum += counts.viewcount
					#print counts.viewcount
		#print viewcountsum
		#print str(extract_date)
		plotdates.append(float(extract_date.strftime('%m-%d').replace("-",".")))
		plotvalues.append(viewcountsum)
		cursor -= 1
	return (plotdates, plotvalues)
