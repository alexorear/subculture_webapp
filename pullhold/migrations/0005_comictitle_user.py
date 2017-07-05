# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-05 03:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pullhold', '0004_pullhold'),
    ]

    operations = [
        migrations.AddField(
            model_name='comictitle',
            name='user',
            field=models.ManyToManyField(related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]