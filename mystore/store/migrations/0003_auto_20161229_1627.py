# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20161229_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, default=None, upload_to=b'store/static'),
        ),
    ]
