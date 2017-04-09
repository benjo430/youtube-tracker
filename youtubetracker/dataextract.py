from datetime import datetime
from datetime import timedelta
from datetime import date


# def getdata(allobject,date1,date2):
# 	# Take an object that contains all the videos and return a tuple with two lists.
# 	# One contains the plot dates, the other the plot values

	
# 	plotdates = []
# 	plotvalues = []
# 	# Create datetimes out of dates from URL - convert the - to ,
# 	startingdatetime = datetime.strptime(date1, '%Y-%m-%d').date() 
# 	#startingdatetime = datetime.datetime(date1.replace("-",","))
# 	endingdatetime = datetime.strptime(date2, '%Y-%m-%d').date() 
# 	dayspread = (endingdatetime - startingdatetime).days
# 	cursor = dayspread



# 	for i in range(dayspread+1):
# 		extract_date = endingdatetime - timedelta(cursor)
# 		#print type(extract_date)
# 		#print "Date: " + str(extract_date)
# 		viewcountsum = 0
# 		for video in allobject:
# 			# Get the all the view counts of this video
# 			viewcounts = Viewcount.objects.all().filter(video=video)
# 			for counts in viewcounts:
# 				if counts.viewcountdate == extract_date:
# 					viewcountsum += counts.viewcount
# 					#print counts.viewcount
# 		#print viewcountsum
# 		print str(extract_date)
# 		plotdates.append(cursor)
# 		plotvalues.append(viewcountsum)
# 		cursor -= 1
# 	return (plotdates, plotvalues)


getdata("nothing","2010-12-23","2011-01-10")