# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse, render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User, Group

from .models import Cutting_phase, Embedding_phase, Polishing_phase, Material_Purchase, Seller
from django.db.models import Sum, Count
import json
from mraurum import settings

from .models import Cutting_phase, Embedding_phase, Polishing_phase, Material_Purchase, Seller, Hallmark_Verification
from django.db.models import Sum, Count
from django.template import loader
from django.http import HttpResponse as HTTPResponse
import json


# Create your views here.

@login_required
def index(request):
    cutting_count = Cutting_phase.objects.filter(receive_date__isnull=True).count()
    embedder_count = Embedding_phase.objects.filter(receive_date__isnull=True).count()
    polishing_count = Polishing_phase.objects.filter(receive_date__isnull=True).count()
    
    context = {
        'cutting_count': cutting_count,
        'embedder_count': embedder_count,
        'polishing_count': polishing_count,
    }
    
    return render(request, 'index.html', context)

@login_required
def get_jewellery_in_progress(request):
    if request.method == 'GET':
        return render(request, 'jewelleryinprocess.html',{})
    code = request.POST.get('progress')
    print(code)
    code = '3'
    
    cutting_progress = Cutting_phase.objects.filter(jewellery_id__id=code)
    if(len(cutting_progress)>0):
        cutting_progress = cutting_progress[0]
    
    embedding_progress = Embedding_phase.objects.filter(jewellery_id__id=code)
    if(len(embedding_progress)>0):
        embedding_progress = embedding_progress[0]
    
    hallmark_progress = Hallmark_Verification.objects.filter(jewellery_id__id=code)
    if(len(hallmark_progress)>0):
        hallmark_progress = hallmark_progress[0]
    
    polishing_progress = Polishing_phase.objects.filter(jewellery_id__id=code)
    if(len(polishing_progress)>0):
        polishing_progress = polishing_progress[0]
    
    seller_progress = Seller.objects.filter(jewellery_id__id=code)
    if(len(seller_progress)>0):
        seller_progress = seller_progress[0]
    
    # print(cutting_progress)
    # print(embedding_progress)
    context = {
        'cutting_progress':cutting_progress,
        'embedding_progress':embedding_progress,
        'polishing_progress':polishing_progress,
        'hallmark_progress':hallmark_progress,
        'seller_progress':seller_progress,
    }
    
    return render(request,'jewelleryinprocess.html', context)

@login_required
def get_charts(request):
    context = {

    }

    return render(request,'jewelleryinprocess.html', context)

@login_required
def get_charts(request):
    context = {

    }

    return render(request, 'charts.html', context)

@login_required
def get_stock(request):
    stock = Material_Purchase.objects.values('material_type_id__material_name','material_type_id__material_purity','material_type_id__material_current_price','material_type_id__material_unit').annotate(total_supply=Sum('purchase_weight'),total_price=Sum('purchase_price')).order_by('purchase_date')
    context = {
        "stocks":stock,
    }
    print(stock)
    return render(request, 'currentstock.html', context)

@login_required
def get_cutters(request):
    cutter = Cutting_phase.objects.filter(receive_date__isnull=False)
    context = {
        "cutter":cutter,
    }
    #print(cutter)
    return render(request, 'cutter.html', context)

@login_required
def get_embedders(request):
    embedder = Embedding_phase.objects.filter(receive_date__isnull=False)
    context = {
        "embedder":embedder,
    }
    return render(request, 'embedder.html', context)

@login_required
def get_polishers(request):
    polisher = Polishing_phase.objects.filter(receive_date__isnull=False)
    context = {
        "polisher":polisher,
    }
    return render(request, 'polisher.html', context)

@login_required
def get_suppliers(request):
    supplier = Material_Purchase.objects.values('supplier_id__username').annotate(total_supply=Sum('purchase_weight'),total_price=Sum('purchase_price')).order_by('purchase_date')
    context = {
        "supplier":supplier,
    }
    return render(request, 'supplier.html', context)

@login_required
def get_sellers(request):
    seller = Seller.objects.values('seller_id__username').annotate(total_supply=Count('seller_id')).order_by('-total_supply')
    context = {
        "seller":seller,
    }
    print(seller)
    return render(request, 'seller.html', context)