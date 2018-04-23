# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User as AdminUser, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import GroupAdmin
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
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

class UserType(Group):
    #user_type = models.CharField(max_length=255, verbose_name='User Type')

    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('User Type')

class User(models.Model):
    name = models.OneToOneField(AdminUser, max_length=255, verbose_name='User Name', null=False)
    user_address = models.TextField(max_length=1000, verbose_name='Address', null=False)
    contact_details_1 = models.CharField(max_length=13, verbose_name='Phone Number 1', null=False)
    contact_details_2 = models.CharField(max_length=13, verbose_name='Phone Number 2', null=True)
    email = models.CharField(max_length=255, verbose_name='EMail ID', null=False)
    rating = IntegerRangeField(help_text='Rating of the User', min_value=1, max_value=10, default=5)

    def __str__(self):
        return self.name.username

    def clean(self):
        if self.rating > 10 or self.rating < 1:
            raise ValidationError("Rating must be between 1 to 10")
        super(User,self).clean()

class Raw_Material_Type(models.Model):
    material_name=models.CharField(max_length=255, verbose_name='Material Name', null=False)
    material_purity=models.PositiveIntegerField(verbose_name='Material Purity',null=False)
    material_current_price=models.FloatField(verbose_name='Current Price',null=False)
    material_unit=models.FloatField(verbose_name='Material Unit',null=False)

    class Meta:
        verbose_name = _("Raw Material Type")
        verbose_name_plural = _("Raw Material Types")

    def __str__(self):
        return self.material_name

class Material_Purchase(models.Model):
    material_type_id=models.ForeignKey(Raw_Material_Type,verbose_name='Material Type', on_delete=None, null=False)
    purchase_price=models.FloatField(verbose_name='Purchase Price',null=False,validators=[MinValueValidator(Decimal('0.01'))])
    purchase_weight=models.FloatField(verbose_name='Purchase Weight',null=False, validators=[MinValueValidator(Decimal('0.01'))])
    purchase_date = models.DateTimeField(verbose_name='Purchase Date',blank=True, null=True)
    supplier_id=models.ForeignKey(AdminUser,verbose_name='Suplier', on_delete=None, null=False)

    class Meta:
        verbose_name = _("Purchase Raw Material")
        verbose_name_plural = _("Purchase Raw Materials")

    def __str__(self):
        return str(self.material_type_id)


class Jewellery_type(models.Model):
    jewellery_name=models.CharField(max_length=255, verbose_name='Jewellery Name', null=False)
    material_type_id=models.ForeignKey(Raw_Material_Type,verbose_name='Material Type', on_delete=None, null=False)

    class Meta:
        verbose_name = _("Jewellery Type")
        verbose_name_plural = _("Jewellery Types")

    def __str__(self):
        return self.jewellery_name

class Design_Catalog(models.Model):
    design_name=models.CharField(max_length=255, verbose_name='Design Name', null=False)
    design_description = models.TextField(max_length=1000, verbose_name='Design Description', null=False)
    jewellery_type = models.ForeignKey(Jewellery_type,verbose_name='Jewellery Type',on_delete=None, null=False)
    catalog_name = models.TextField(verbose_name='Catalog Name and Desc', null=False, blank=False)
    added_date = models.DateField(verbose_name='Added Date',blank=True, null=True)
    image = models.ImageField(verbose_name='Design photo',null=False, blank=False)

    class Meta:
        verbose_name = _("Design")
        verbose_name_plural = _("Designs")

    def __str__(self):
        return self.design_name

class Jewel(models.Model):
    jewel_name=models.CharField(max_length=255, verbose_name='Jewel Name', null=False)

    class Meta:
        verbose_name = _("Jewel")
        verbose_name_plural = _("Jewels")

    def __str__(self):
        return self.jewel_name

class Jewellery(models.Model):
    design_id= models.ForeignKey(Design_Catalog,verbose_name='Jewellery Design',on_delete=None, null=False)    
    raw_material_id=models.ForeignKey(Raw_Material_Type,verbose_name='Raw Material',on_delete=None, null=False)

    class Meta:
        verbose_name = _("Jewellery")
        verbose_name_plural = _("Jewelleries") 
    
    def __str__(self):
        return str(self.design_id) + str(self.raw_material_id)


class Cutting_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    cutter_id=models.ForeignKey(AdminUser,verbose_name='Cutter Name',on_delete=None, null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    cutting_cost=models.PositiveIntegerField(verbose_name='Cutting Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    sent_date= models.DateField(verbose_name='Sent Date')
    receive_date= models.DateField(verbose_name='Receive Date')

    class Meta:
        verbose_name = _("Cutting Phase")
        verbose_name_plural = _("Cutting Phases")
        unique_together = ('jewellery_id','cutter_id','sent_date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.cutter_id)
    
    def clean(self):
        if self.receive_date < self.sent_date:
            raise ValidationError("Receving date cannot be smaller than Sending Date")
        if self.receive_weight > self.weight_sent:
            raise ValidationError("Receving weight cannot be larger than Sent weight")
        super(Cutting_phase,self).clean()

class Embedding_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    embedder_id=models.ForeignKey(AdminUser,verbose_name='Embedder Name',on_delete=None, null=False)
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

    class Meta:
        verbose_name = _("Embedding Phase")
        verbose_name_plural = _("Embedding Phases")
        unique_together = ('jewellery_id','embedder_id','sent_date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.embedder_id)
    
    def clean(self):
        if self.receive_date < self.sent_date:
            raise ValidationError("Receving date cannot be smaller than Sending Date")
        if self.receive_weight < self.weight_sent:
            raise ValidationError("Receving weight cannot be smaller than Sent weight")
        super(Embedding_phase,self).clean()

class Polishing_phase(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    polisher_id=models.ForeignKey(AdminUser,verbose_name='Polisher Name',on_delete=None, null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    polishing_cost=models.PositiveIntegerField(verbose_name='polishing Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    sent_date= models.DateField(verbose_name='Sent Date')
    receive_date= models.DateField(verbose_name='Receive Date')

    class Meta:
        verbose_name = _("Polishing Phase")
        verbose_name_plural = _("Polishing Phases")
        unique_together = ('jewellery_id','polisher_id','sent_date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.polisher_id)
    
    def clean(self):
        if self.receive_date < self.sent_date:
            raise ValidationError("Receving date cannot be smaller than Sending Date")
        if self.receive_weight > self.weight_sent:
            raise ValidationError("Receving weight cannot be larger than Sent weight")
        super(Polishing_phase,self).clean()

class Seller(models.Model):
    seller_id = models.ForeignKey(AdminUser,verbose_name='Seller Name',on_delete=None, null=False)
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    order_receive_date = models.DateField(verbose_name='Order Receive Date')
    order_send_date = models.DateField(verbose_name='Order Send Date',blank=True,null=True)
    payment_received = models.FloatField(default=0.0,verbose_name='Amount of payment received', blank=True, null=True)


    class Meta:
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")
        unique_together = ('seller_id','jewellery_id','order_send_date')

    def __str__(self):
        return str(self.jewellery_id) + str(self.seller_id)

    def clean(self):
        if self.order_send_date is not None and self.order_receive_date > self.order_send_date:
            raise ValidationError("Receving date cannot be greater than Sending Date")
        if self.order_send_date is not None and Polishing_phase.receive_date is None or Embedding_phase.receive_date is None or Cutting_phase.receive_date is None:
            raise ValidationError("Must have been sent to Cutter, Embedder and Polisher")
        super(Seller,self).clean()

class Hallmark_Verification(models.Model):
    jewellery_id=models.ForeignKey(Jewellery,verbose_name='Jewellery',on_delete=None, null=False)
    order_receive_date = models.DateField(verbose_name='Order Receive Date')
    order_send_date = models.DateField(verbose_name='Order Send Date',blank=True,null=True)
    verifying_cost=models.PositiveIntegerField(verbose_name='Verifying Cost',null=False)
    other_cost=models.PositiveIntegerField(verbose_name='Other Cost',null=False)
    weight_sent=models.FloatField(default=0.0,verbose_name='Weight Sent')
    receive_weight=models.FloatField(default=0.0,verbose_name='Receive Weight')
    status = models.BooleanField(verbose_name='Verification Status')
    remark = models.TextField(max_length=1000, verbose_name='Remark', null=True, blank=True)

    class Meta:
        verbose_name = _("Hallmark Verification Phase")
        verbose_name_plural = _("Hallmark Verification Phases")
        unique_together = ('jewellery_id','order_send_date')

    def __str__(self):
        return str(self.jewellery_id)
    
    def clean(self):
        if self.receive_date < self.sent_date:
            raise ValidationError("Receving date cannot be smaller than Sending Date")
        if self.receive_weight > self.weight_sent:
            raise ValidationError("Receving weight cannot be larger than Sent weight")
        super(Hallmark_Verification,self).clean()