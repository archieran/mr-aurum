# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 06:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jmms', '0009_raw_material_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material_Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_price', models.PositiveIntegerField(verbose_name='Purchase Price')),
                ('purchase_weight', models.PositiveIntegerField(verbose_name='Purchase Weight')),
                ('purchase_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='raw_material_type',
            name='material_purity',
            field=models.PositiveIntegerField(verbose_name='Material Purity'),
        ),
        migrations.AddField(
            model_name='material_purchase',
            name='material_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jmms.Raw_Material_Type'),
        ),
        migrations.AddField(
            model_name='material_purchase',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jmms.User'),
        ),
    ]