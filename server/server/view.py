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
    else:
        request.session['user_name'] = "admin"
    context["session_key"] = request.session.session_key
    return render(request, 'rh_detail.html', context)
#host/city/area_id/rh/
def show_rh_list(request):
    context = {}
    privince = ""
    city = ""
    area = ""
    price = ""
    bed = ""
    str_type = ""
    prop = ""

    '''
    '''
    if "prov" in request.GET:
        privince = request.GET['prov']
    if "city" in request.GET:
        city = request.GET['city']
    if "area" in request.GET:
        area = request.GET['area']
    if "price" in request.GET:
        price = request.GET['price']
    if "bed" in request.GET:
        bed = request.GET['bed']
    if "type" in request.GET:
        str_type = request.GET['type']
    if "prop" in request.GET:
        prop = request.GET['prop']
    # FIXME
    get_rh_list(context, privince, city, area, price, bed, str_type, prop)

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

'''
'''
def get_price_q_query(price):
    if price == '1':
        price_filter = (Q(rh_charges_min__gte=0) & Q(rh_charges_min__lte=1000)) | (Q(rh_charges_max__gte=0) & Q(rh_charges_max__lte=1000))
    elif price == '2':
        price_filter = (Q(rh_charges_min__gte=1000) & Q(rh_charges_min__lte=2000)) | (Q(rh_charges_max__gte=1000) & Q(rh_charges_max__lte=2000))
    elif price == '3':
        price_filter = (Q(rh_charges_min__gte=2000) & Q(rh_charges_min__lte=3000)) | (Q(rh_charges_max__gte=2000) & Q(rh_charges_max__lte=3000))
    elif price == '4':
        price_filter = (Q(rh_charges_min__gte=3000) & Q(rh_charges_min__lte=5000)) | (Q(rh_charges_max__gte=3000) & Q(rh_charges_max__lte=5000))
    elif price == '5':
        price_filter = (Q(rh_charges_min__gte=5000) & Q(rh_charges_min__lte=10000)) | (Q(rh_charges_max__gte=5000) & Q(rh_charges_max__lte=10000))
    elif price == '6':
        price_filter = Q(rh_charges_min__gte=10000) | Q(rh_charges_max__gte=10000)
    else:
        # FIXME
        price_filter = None
    return price_filter

def get_bednum_q_query(bednum):
    if bednum == '1':
        bednum_int_filter = Q(rh_bednum_int__lt=50)
    elif bednum == '2':
        bednum_int_filter = Q(rh_bednum_int__gte=50) & Q(rh_bednum_int__lt=100)
    elif bednum == '3':
        bednum_int_filter = Q(rh_bednum_int__gte=100) & Q(rh_bednum_int__lt=200)
    elif bednum == '4':
        bednum_int_filter = Q(rh_bednum_int__gte=200) & Q(rh_bednum_int__lt=300)
    elif bednum == '5':
        bednum_int_filter = Q(rh_bednum_int__gte=300) & Q(rh_bednum_int__lt=500)
    elif bednum == '6':
        bednum_int_filter = Q(rh_bednum_int__gte=500)
    else:
        # FIXME
        bednum_int_filter = None
    return bednum_int_filter

def get_rh_list(context, privince, city, area, price, bed, str_type, prop):
    # FIXME, should not query all DB
    # db = rh.objects.filter(Q(rh_area__endswith="门头沟区"))
    all_filter = Q(rh_area__endswith="海淀区")
    if len(bed) != 0 and bed != '0':
        bednum_filter = get_bednum_q_query(bed)
        all_filter = all_filter & bednum_filter
    if len(price) != 0 and price != '0':
        price_filter = get_price_q_query(price)
        all_filter = all_filter & price_filter
    db = rh.objects.filter(all_filter)

    context['records'] = db
    context['message'] = "privince: " + privince
    context['message'] = context['message'] + ", city: " + city
    context['message'] = context['message'] + ", area: "+ area
    context['message'] = context['message'] + ", price: "+ str(price)
    context['message'] = context['message'] + ", bed: "+ str(bed)
    context['message'] = context['message'] + ", str_type: " + str(str_type)
    context['message'] = context['message'] + ", prop: "+ str(prop)
    print(context['message'])

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
