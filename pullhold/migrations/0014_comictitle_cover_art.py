# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pullhold', '0013_auto_20170709_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='comictitle',
            name='cover_art',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]