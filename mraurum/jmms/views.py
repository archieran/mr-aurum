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
from django.db.models.functions import ExtractMonth as Month
from mraurum import settings

from .models import Cutting_phase, Embedding_phase, Polishing_phase, Material_Purchase, Seller, Hallmark_Verification
from django.db.models import Sum, Count
from django.template import loader
from django.http import HttpResponse as HTTPResponse
import json
from datetime import date

# Create your views here.

@login_required
def index(request):
    cutting_count = Cutting_phase.objects.filter(receive_date__isnull=True).count()
    embedder_count = Embedding_phase.objects.filter(receive_date__isnull=True).count()
    polishing_count = Polishing_phase.objects.filter(receive_date__isnull=True).count()
    verification_count = Hallmark_Verification.objects.filter(order_receive_date__isnull=True).count()

    cutting_count_today = Cutting_phase.objects.filter(receive_date = date.today()).count()
    embedding_count_today = Embedding_phase.objects.filter(receive_date = date.today()).count()
    polishing_count_today = Polishing_phase.objects.filter(receive_date = date.today()).count()
    verification_count_today = Hallmark_Verification.objects.filter(order_receive_date = date.today()).count()

    cutter_count = User.objects.filter(groups__name='Cutter').count()
    embedder_count = User.objects.filter(groups__name='Embedder').count()
    polisher_count = User.objects.filter(groups__name='Polisher').count()
    supplier_count = User.objects.filter(groups__name='Raw Material Supplier').count()
    seller_count = User.objects.filter(groups__name='Seller').count()
    
    stock = Material_Purchase.objects.values('material_type_id__material_name','material_type_id__material_purity').annotate(total_supply=Sum('purchase_weight'),total_price=Sum('purchase_price'))
    gold_24_stock = stock.filter(material_type_id__material_name='Gold',material_type_id__material_purity='24')
    if(len(gold_24_stock)>0):
        gold_24_stock = gold_24_stock[0]
    
    gold_22_stock = stock.filter(material_type_id__material_name='Gold',material_type_id__material_purity='22')
    if(len(gold_22_stock)>0):
        gold_22_stock = gold_22_stock[0]
    
    gold_18_stock = stock.filter(material_type_id__material_name='Gold',material_type_id__material_purity='18')
    if(len(gold_18_stock)>0):
        gold_18_stock = gold_18_stock[0]
    
    silver_24_stock = stock.filter(material_type_id__material_name='Silver')
    if(len(silver_24_stock)>0):
        silver_24_stock = silver_24_stock[0]
    
    context = {
        'cutting_count': cutting_count,
        'embedder_count': embedder_count,
        'polishing_count': polishing_count,
        'verification_count': verification_count,
        'cutting_count_today': cutting_count_today,
        'embedding_count_today': embedding_count_today,
        'polishing_count_today': polishing_count_today,
        'verification_count_today': verification_count_today,
        'cutter_count': cutter_count,
        'embedder_count': embedder_count,
        'polisher_count':polisher_count,
        'supplier_count': supplier_count,
        'seller_count': seller_count,
        'gold_24_stock': gold_24_stock,
        'gold_22_stock': gold_22_stock,
        'gold_18_stock': gold_18_stock,
        'silver_24_stock': silver_24_stock,
        'active_tab': 'dashboard',
    }
    
    return render(request, 'index.html', context)

@login_required
def get_jewellery_in_progress(request):
    if request.method == 'GET':
        context = {
            'active_tab': 'jinprocess',
        }
        return render(request, 'jewelleryinprocess.html',context)
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
        'active_tab': 'jinprocess',
    }
    
    return render(request,'jewelleryinprocess.html', context)

@login_required
def get_charts(request):
    total_cutting_gold_sent = Cutting_phase.objects.annotate(mon=Month('sent_date')).values('mon').annotate(total_sent=Sum('weight_sent')).order_by('mon')
    total_cutting_gold_recv = Cutting_phase.objects.annotate(mon=Month('receive_date')).values('mon').annotate(total_rec=Sum('receive_weight')).order_by('mon')
    print(total_cutting_gold_recv)

    # total_embed_gold_sent = Embedding_phase.objects.values('weight_sent').annotate(total_sent=Sum('weight_sent'))[0]
    # total_embed_gold_recv = Embedding_phase.objects.values('receive_weight').annotate(total_rec=Sum('receive_weight'))[0]
    # waste_emd = float(total_embed_gold_recv["total_rec"]) - float(total_embed_gold_sent["total_sent"])

    # total_poli_gold_sent = Polishing_phase.objects.values('weight_sent').annotate(total_sent=Sum('weight_sent'))[0]
    # total_poli_gold_recv = Polishing_phase.objects.values('receive_weight').annotate(total_rec=Sum('receive_weight'))[0]
    # waste_pol = float(total_poli_gold_sent["total_sent"]) - float(total_poli_gold_recv["total_rec"])

    # total_veri_gold_sent = Hallmark_Verification.objects.values('weight_sent').annotate(total_sent=Sum('weight_sent'))
    # if(len(total_veri_gold_sent)>0):
    #     total_veri_gold_sent = total_veri_gold_sent[0]
    
    # total_veri_gold_recv = Hallmark_Verification.objects.values('receive_weight').annotate(total_rec=Sum('receive_weight'))
    # if(len(total_veri_gold_recv)>0):
    #     total_veri_gold_recv = total_veri_gold_recv[0]

    # waste_veri = float(total_veri_gold_sent["total_sent"]) - float(total_veri_gold_recv["total_rec"])

    context = {
        'active_tab': 'charts',
    }

    return render(request,'charts.html', context)

@login_required
def get_stock(request):
    stock = Material_Purchase.objects.values('material_type_id__material_name','material_type_id__material_purity','material_type_id__material_current_price','material_type_id__material_unit').annotate(total_supply=Sum('purchase_weight'),total_price=Sum('purchase_price')).order_by('purchase_date')
    context = {
        "stocks":stock,
        'active_tab': 'stock',
    }
    print(stock)
    return render(request, 'currentstock.html', context)

@login_required
def get_cutters(request):
    cutter = Cutting_phase.objects.filter(receive_date__isnull=False)
    context = {
        "cutter":cutter,
        'active_tab': 'user_cutter',
    }
    #print(cutter)
    return render(request, 'cutter.html', context)

@login_required
def get_embedders(request):
    embedder = Embedding_phase.objects.filter(receive_date__isnull=False)
    context = {
        "embedder":embedder,
        'active_tab': 'user_embedder',
    }
    return render(request, 'embedder.html', context)

@login_required
def get_polishers(request):
    polisher = Polishing_phase.objects.filter(receive_date__isnull=False)
    context = {
        "polisher":polisher,
        'active_tab': 'user_polisher',
    }
    return render(request, 'polisher.html', context)

@login_required
def get_suppliers(request):
    supplier = Material_Purchase.objects.values('supplier_id__username').annotate(total_supply=Sum('purchase_weight'),total_price=Sum('purchase_price')).order_by('purchase_date')
    context = {
        "supplier":supplier,
        'active_tab': 'user_supplier',
    }
    return render(request, 'supplier.html', context)

@login_required
def get_sellers(request):
    seller = Seller.objects.values('seller_id__username').annotate(total_supply=Count('seller_id')).order_by('-total_supply')
    context = {
        "seller":seller,
        'active_tab': 'user_supplier',
    }
    print(seller)
    return render(request, 'seller.html', context)