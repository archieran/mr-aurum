# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmms', '0012_auto_20180324_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jewel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jewel_name', models.CharField(max_length=255, verbose_name='Jewel Name')),
            ],
        ),
    ]