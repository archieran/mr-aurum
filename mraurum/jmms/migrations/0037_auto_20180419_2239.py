# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-19 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jmms', '0036_auto_20180419_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hallmark_Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_receive_date', models.DateField(verbose_name='Order Receive Date')),
                ('order_send_date', models.DateField(blank=True, null=True, verbose_name='Order Send Date')),
                ('verifying_cost', models.PositiveIntegerField(verbose_name='Verifying Cost')),
                ('other_cost', models.PositiveIntegerField(verbose_name='Other Cost')),
                ('weight_sent', models.FloatField(default=0.0, verbose_name='Weight Sent')),
                ('receive_weight', models.FloatField(default=0.0, verbose_name='Receive Weight')),
                ('remark', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Remark')),
                ('jewellery_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jmms.Jewellery', verbose_name='Jewellery')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_receive_date', models.DateField(verbose_name='Order Receive Date')),
                ('order_send_date', models.DateField(blank=True, null=True, verbose_name='Order Send Date')),
                ('payment_received', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Amount of payment received')),
                ('jewellery_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jmms.Jewellery', verbose_name='Jewellery')),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Seller Name')),
            ],
        ),
        migrations.RemoveField(
            model_name='design_catalog',
            name='added_date_time',
        ),
        migrations.AddField(
            model_name='design_catalog',
            name='added_date',
            field=models.DateField(blank=True, null=True, verbose_name='Added Date'),
        ),
        migrations.AddField(
            model_name='design_catalog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Design photo'),
        ),
    ]