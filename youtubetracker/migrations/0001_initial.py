# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 00:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marketer', models.CharField(choices=[('Jacob', 'Jacob'), ('Angie', 'Angie'), ('Emily', 'Emily'), ('Louise', 'Louise')], default='Jacob', max_length=30)),
                ('url', models.URLField()),
                ('community', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Viewcount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewcountdate', models.DateField()),
                ('viewcount', models.IntegerField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtubetracker.Video')),
            ],
        ),
    ]
