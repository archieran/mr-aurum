# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 11:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jmms', '0015_cutting_phase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cutting_phase',
            name='cutter_id',
        ),
        migrations.RemoveField(
            model_name='cutting_phase',
            name='jewellery_id',
        ),
        migrations.DeleteModel(
            name='Cutting_Phase',
        ),
    ]