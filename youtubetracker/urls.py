from django.conf.urls import url

from . import views

app_name = 'youtubetracker'

urlpatterns = [
    # ex: /youtubetracker/5/
    url(r'^$', views.home, name='index'),

    # ex: /youtubetracker/2017-04-01/2017-04-06/
    # url(r'^(?P<date1>\d{4}-\d{2}-\d{2})/(?P<date2>\d{4}-\d{2}-\d{2})/(?P<pubdate1>\d{4}-\d{2}-\d{2})/(?P<pubdate2>\d{4}-\d{2}-\d{2})/$', views.index, name='index'),
    
    # ex: /youtubetracker/5/
    url(r'^(?P<video_id>[0-9]+)/$', views.detail, name='detail'),

    # ex: /youtubetracker/Jacob/marketer
    url(r'^(?P<marketer_id>[\w\-]+)/marketer/$', views.marketerdetail, name='marketerdetail'),

    # ex: /youtubetracker/Jacob/marketer/2017-04-01/2017-04-06/
    url(r'^(?P<marketer_id>[\w\-]+)/marketer/(?P<date1>\d{4}-\d{2}-\d{2})/(?P<date2>\d{4}-\d{2}-\d{2})/(?P<pubdate1>\d{4}-\d{2}-\d{2})/(?P<pubdate2>\d{4}-\d{2}-\d{2})/$', views.marketerdetail, name='marketerdetail'),

    # youtubetracker/all/incremental/date1/date2/pubdate1/pubdate2
    # http://127.0.0.1:8000/youtubetracker/all/incremental/2017-03-01/2017-04-08/2017-03-01/2017-04-08
    url(r'^(?P<viewby>[\w\-]+)/(?P<chartdisplay>[\w\-]+)/(?P<date1>\d{4}-\d{2}-\d{2})/(?P<date2>\d{4}-\d{2}-\d{2})/(?P<pubdate1>\d{4}-\d{2}-\d{2})/(?P<pubdate2>\d{4}-\d{2}-\d{2})/$', views.index, name='index'),

]