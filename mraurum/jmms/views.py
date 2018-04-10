# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse, render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cutting_phase, Embedding_phase, Polishing_phase

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