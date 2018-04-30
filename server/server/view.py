# -*- coding: utf-8 -*-
 
import sys

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from rh.models import rh

sys.path.append("../")
sys.path.append("../../")

curr_index = 0

def start(request):
    global curr_index
    context = {}
    if "pre_page" in request.POST:
        get_pre_page(context)
    if "next_page" in request.POST:
        get_next_page(context)
    if "q_id" in request.POST:
        get_page_from_rh_ylw_id(context, request.POST['q_id'])
    if "q_name" in request.POST:
        get_page_from_rh_name(context, request.POST['q_name'])

    return render(request, 'index.html', context)

def show_rh_detail(request):
    context = {}
    if "rhid" in request.GET:
        get_page_from_rh_id(context, request.GET['rhid'])
    if "user_name" in request.session:
        context["user_name"] = request.session['user_name']
        context["session_key"] = request.session.session_key
    else:
        request.session['user_name'] = "admin"
    return render(request, 'rh_detail.html', context)

def show_rh_list(request):
    context = {}
    area = ""
    pr = ""
    bed = ""
    str_type = ""
    prop = ""
    if "area" in request.GET:
        area = request.GET['area']
    if "pr" in request.GET:
        pr = request.GET['pr']
    if "bed" in request.GET:
        bednum = request.GET['bed']
    if "type" in request.POST:
        str_type = request.GET['type']
    if "prop" in request.POST:
        prop = request.GET['prop']
    # FIXME
    get_rh_list(context, area, pr, bed, str_type, prop)

    return render(request, 'rh_list.html', context)

def edit(request):
    global curr_index
    context = {}
    if "pre_page" in request.POST:
        get_pre_page(context)
    if "next_page" in request.POST:
        get_next_page(context)
    if "q_id" in request.POST:
        get_page_from_rh_ylw_id(context, request.POST['q_id'])
    if "q_name" in request.POST:
        get_page_from_rh_name(context, request.POST['q_name'])

    # FIXME
    get_next_page(context)

    return render(request, 'edit.html', context)

def get_pre_page(context):
    global curr_index
    context['message'] = 'pre_page'
    curr_index = curr_index - 1
    # FIXME, should not query all DB
    db = rh.objects.all()
    if curr_index <= 0:
        curr_index = 0
    context['record'] = db[curr_index]

def get_rh_list(context, area, pr, bed, str_type, prop):
    global curr_index
    # FIXME, should not query all DB
    db = rh.objects.filter(Q(rh_area__endswith="门头沟区"))
    curr_index = curr_index + 1
    context['records'] = db
    context['message'] = len(db)

def get_next_page(context):
    global curr_index
    context['message'] = 'next_page'
    # FIXME, should not query all DB
    db = rh.objects.all()
    curr_index = curr_index + 1
    context['records'] = db

def get_page_from_rh_id(context, rh_id):
    context['message'] = 'you are querying rh_id: ' + rh_id
    db = rh.objects.filter(id=rh_id)
    if len(db) > 0:
        # FIXME, should not query only one
        context['record'] = db[0]
    else:
        context['message'] = context['message'] + ', Not Existed'

def get_page_from_rh_ylw_id(context, ylw_id):
    context['message'] = 'you are querying ylw id: ' + ylw_id
    db = rh.objects.filter(rh_ylw_id=ylw_id)
    if len(db) > 0:
        # FIXME, should not query only one
        context['record'] = db[0]
    else:
        context['message'] = context['message'] + ', Not Existed'

def get_page_from_rh_name(context, rh_name):
    context['message'] = 'you are querying yly name: ' + rh_name
    db = rh.objects.filter(rh_name=rh_name)
    if len(db) > 0:
        # FIXME, should not query only one
        context['record'] = db[0]
    else:
        context['message'] = context['message'] + ', Not Existed'

def search(request):
    return start(request)
