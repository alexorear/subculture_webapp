# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pullhold', '0017_auto_20170712_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='comictitle',
            name='thumb_art',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
