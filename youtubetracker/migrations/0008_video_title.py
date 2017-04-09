# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtubetracker', '0007_auto_20170404_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default='No Title Entered', max_length=200),
        ),
    ]
