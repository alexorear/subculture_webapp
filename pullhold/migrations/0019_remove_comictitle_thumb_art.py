# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pullhold', '0018_comictitle_thumb_art'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comictitle',
            name='thumb_art',
        ),
    ]
