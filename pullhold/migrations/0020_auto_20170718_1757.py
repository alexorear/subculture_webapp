# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pullhold', '0019_remove_comictitle_thumb_art'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comictitle',
            name='cover_art',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
