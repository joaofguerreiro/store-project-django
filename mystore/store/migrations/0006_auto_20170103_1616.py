# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20170103_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accordion',
            name='photo',
            field=models.ImageField(blank=True, default=None, upload_to=b'accordions/'),
        ),
    ]
