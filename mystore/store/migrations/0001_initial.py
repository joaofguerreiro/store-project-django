# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accordion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100)),
                ('logo', models.ImageField(default=None, upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='accordion',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Brand'),
        ),
    ]
