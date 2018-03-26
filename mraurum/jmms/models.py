# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


# Create your models here.

class UserType(models.Model):
    user_type = models.CharField(max_length=255, verbose_name='User Type')

    def __str__(self):
        return self.user_type
    def __unicode__(self):
        return self.user_type

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='User Name', null=False)
    user_type = models.ForeignKey(UserType, on_delete=None, null=False)
    user_address = models.TextField(max_length=1000, verbose_name='Address', null=False)
    contact_details_1 = models.CharField(max_length=13, verbose_name='Phone Number 1', null=False)
    contact_details_2 = models.CharField(max_length=13, verbose_name='Phone Number 2', null=True)
    email = models.CharField(max_length=255, verbose_name='EMail ID', null=False)
    rating = IntegerRangeField(help_text='Rating of the User', min_value=1, max_value=10, default=5)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

    def clean(self):
        if self.rating > 10 or self.rating < 1:
            raise ValidationError("Rating must be between 1 to 10")
        super(User,self).clean()

class Raw_Material_Type(models.Model):
    material_name=models.CharField(max_length=255, verbose_name='Material Name', null=False)
    material_purity=models.PositiveIntegerField(verbose_name='Material Purity',null=False)
    material_current_price=models.PositiveIntegerField(verbose_name='Current Price',null=False)
    material_unit=models.PositiveIntegerField(verbose_name='Material Unit',null=False)

    def __str__(self):
        return self.material_name
    def __unicode__(self):
        return self.material_name

class Material_Purchase(models.Model):
    material_type_id=models.ForeignKey(Raw_Material_Type,verbose_name='Material Type', on_delete=None, null=False)
    purchase_price=models.PositiveIntegerField(verbose_name='Purchase Price',null=False)
    purchase_weight=models.PositiveIntegerField(verbose_name='Purchase Weight',null=False)
    purchase_date = models.DateTimeField(verbose_name='Purchase Date',blank=True, null=True)
    supplier_id=models.ForeignKey(User,verbose_name='Suplier', on_delete=None, null=False)

    def __str__(self):
        return str(self.material_type_id)
    def __unicode__(self):
        return str(self.material_type_id)


class Jewellery_type(models.Model):
    jewellery_name=models.CharField(max_length=255, verbose_name='Jewellery Name', null=False)
    material_type_id=models.ForeignKey(Raw_Material_Type,verbose_name='Material Type', on_delete=None, null=False)

    def __str__(self):
        return self.jewellery_name
    def __unicode__(self):
        return self.jewellery_name

class Design_Catalog(models.Model):
    design_name=models.CharField(max_length=255, verbose_name='Design Name', null=False)
    design_description = models.TextField(max_length=1000, verbose_name='Design Description', null=False)
    jewellery_type = models.ForeignKey(Jewellery_type,verbose_name='Jewellery Type',on_delete=None, null=False)
    added_date_time = models.DateTimeField(verbose_name='Added Date & Time',blank=True, null=True)

    def __str__(self):
        return self.design_name
    def __unicode__(self):
        return self.design_name

class Jewel(models.Model):
    jewel_name=models.CharField(max_length=255, verbose_name='Jewel Name', null=False)

    def __str__(self):
        return self.jewel_name
    def __unicode__(self):
        return self.jewel_name

class Jewellery(models.Model):
    design_id= models.ForeignKey(Design_Catalog,verbose_name='Jewellery Design',on_delete=None, null=False)    
    raw_material_id=models.ForeignKey(Raw_Material_Type,verbose_name='Raw Material',on_delete=None, null=False)    
    
    def __str__(self):
        return str(self.design_id) + str(self.raw_material_id)
    def __unicode__(self):
        return str(self.design_id) + str(self.raw_material_id)


class Cutting_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    cutter_id=models.ForeignKey(User,verbose_name='Cutter Name',on_delete=None, null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    cutting_cost=models.PositiveIntegerField(verbose_name='Cutting Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    sent_date= models.DateField(verbose_name='Sent Date')
    receive_date= models.DateField(verbose_name='Receive Date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.cutter_id)
    def __unicode__(self):
        return str(self.jewellery_id) + str(self.cutter_id)

class Embedding_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    embedder_id=models.ForeignKey(User,verbose_name='Embedder Name',on_delete=None, null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    jewel_id=models.ForeignKey(Jewel,verbose_name='Jewel',on_delete=None, null=False)
    jewel_price=models.PositiveIntegerField(verbose_name='Jewel Price',null=False)
    jewel_quantity=models.PositiveIntegerField(verbose_name='Jewel Quantity',null=False)
    jewel_weight=models.FloatField(default=0.0,verbose_name='Jewel Weight')
    jewel_size=models.PositiveIntegerField(verbose_name='Jewel Size',null=False)
    embedding_cost=models.PositiveIntegerField(verbose_name='embedding Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    sent_date= models.DateField(verbose_name='Sent Date')
    receive_date= models.DateField(verbose_name='Receive Date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.embedder_id)
    def __unicode__(self):
        return str(self.jewellery_id) + str(self.embedder_id)

class Polishing_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    polisher_id=models.ForeignKey(User,verbose_name='Polisher Name',on_delete=None, null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    polishing_cost=models.PositiveIntegerField(verbose_name='polishing Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    sent_date= models.DateField(verbose_name='Sent Date')
    receive_date= models.DateField(verbose_name='Receive Date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.polisher_id)
    def __unicode__(self):
        return str(self.jewellery_id) + str(self.polisher_id)
