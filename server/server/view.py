# -*- coding: utf-8 -*-
 
import sys

from django.http import HttpResponse
from django.shortcuts import render

from RHModel.models import rh
 
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

def get_next_page(context):
    global curr_index
    context['message'] = 'next_page'
    # FIXME, should not query all DB
    db = rh.objects.all()
    curr_index = curr_index + 1
    context['record'] = db[curr_index]

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

'''
def start(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
