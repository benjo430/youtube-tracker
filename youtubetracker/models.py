from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Video(models.Model):
	UNKNOWN = 'Unknown'
	JACOB = 'Jacob'
	ANGIE = 'Angie'
	EMILY = 'Emily'
	LOUISE = 'Louise'
	TYLER = 'Tyler'
	SARAH = 'Sarah'
	MELISSA = 'Melissa'
	VALERIA = 'Valeria'
	MAURICIO = 'Mauricio'
	NOOR = 'Noor'
	BEN = 'Ben'
	ANNIE = 'Annie'
	JULIANA = 'Juliana'
	TOBY = 'Toby'

	MARKETER = (
		(UNKNOWN, 'Unknown'),
		(JACOB, 'Jacob'),
		(ANGIE, 'Angie'),
		(EMILY, 'Emily'),
		(LOUISE, 'Louise'),
		(TYLER, 'Tyler'),
		(SARAH, 'Sarah'),
		(MELISSA, 'Melissa'),
		(VALERIA, 'Valeria'),
		(MAURICIO, 'Mauricio'),
		(NOOR, 'Noor'),
		(BEN, 'Ben'),
		(ANNIE, 'Annie'),
		(JULIANA, 'Juliana'),
		(TOBY, 'Toby'),

	)
	marketer = models.CharField(
		max_length=30,
		choices=MARKETER,
		default=UNKNOWN,
	)

	EN = 'English'
	PT = 'Portuguese'
	ES = 'Spanish'
	AR = 'Arabic'
	RU = 'Russian'

	LANGUAGES = (
		(EN, 'EN'),
		(PT, 'PT'),
		(ES, 'ES'),
		(AR, 'AR'),
		(RU, 'RU'),
	)
	language = models.CharField(
		max_length=30,
		choices=LANGUAGES,
		default=EN,
	)

	url = models.URLField(max_length=200, unique=True)
	community = models.CharField(max_length=50)
	cost = models.IntegerField()
	publishdate = models.DateField(auto_now=False, auto_now_add=False)
	title = models.CharField(max_length=200, default="No Title Entered")
	projectedviews = models.IntegerField(default=0)
	def __str__(self):
		return self.url

class Viewcount(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	viewcountdate = models.DateField(auto_now=False, auto_now_add=False)
	viewcount = models.IntegerField()
	def __str__(self):
		return self.viewcount


