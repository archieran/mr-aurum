# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 06:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jmms', '0007_raw_material_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Raw_Material_Type',
        ),
    ]