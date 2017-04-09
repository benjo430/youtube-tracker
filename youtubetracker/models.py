from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Video(models.Model):
	JACOB = 'Jacob'
	ANGIE = 'Angie'
	EMILY = 'Emily'
	LOUISE = 'Louise'

	MARKETER = (
		(JACOB, 'Jacob'),
		(ANGIE, 'Angie'),
		(EMILY, 'Emily'),
		(LOUISE, 'Louise'),
	)
	marketer = models.CharField(
		max_length=30,
		choices=MARKETER,
		default=JACOB,
	)

	url = models.URLField(max_length=200, unique=True)
	community = models.CharField(max_length=50)
	cost = models.IntegerField()
	publishdate = models.DateField(auto_now=False, auto_now_add=False)
	title = models.CharField(max_length=200, default="No Title Entered")
	def __str__(self):
		return self.url

class Viewcount(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	viewcountdate = models.DateField(auto_now=False, auto_now_add=False)
	viewcount = models.IntegerField()
	def __str__(self):
		return self.viewcount
