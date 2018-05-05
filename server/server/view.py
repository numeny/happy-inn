# -*- coding: utf-8 -*-
 
import sys

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from rh.models import rh
from rh.models import city

from json_response import JsonResponse

sys.path.append("../")
sys.path.append("../../")

curr_index = 0
rh_num_per_page = 15
g_area_map = {}
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
'''
'''
def init_g_area_map_if_neccesary():
    global g_area_map
    if g_area_map is not None and len(g_area_map) != 0:
        return
    #FIXME, get cities from where? rh or city's db
    areas = city.objects.order_by('privince', 'city', 'area').values('privince', 'city', 'area').distinct()
    for r in areas:
        if len(r['privince']) == 0 or len(r['city']) == 0 or len(r['area']) == 0:
            print("city's field is null. [%s] [%s] [%s]"\
                % (r['privince'].encode('utf-8'), r['city'].encode('utf-8'), r['area'].encode('utf-8')))
            continue;
        if not g_area_map.has_key(r['privince']):
            privince_map = {}
            g_area_map.setdefault(r['privince'], privince_map)
        privince_map = g_area_map.get(r['privince'])

        if not privince_map.has_key(r['city']):
            city_list = []
            privince_map.setdefault(r['city'], city_list)
        city_list = privince_map.get(r['city'])
        city_list.append(r['area'])

def getAreaList(privince, city):
    global g_area_map

    init_g_area_map_if_neccesary()

    if privince is None or len(privince) == 0:
        return g_area_map.keys()

    if not g_area_map.has_key(privince):
        print("Error: area map has no privince[%s]" % privince)
        return []

    privince_map = g_area_map.get(privince)
    if city is None or len(city) == 0:
        return privince_map.keys()

    if not privince_map.has_key(city):
        print("Error: area map has no privince[%s] city[%s] " % (privince, city))
        return []
    return privince_map.get(city)

def citylist(request):
    '''
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)
    '''
    a = range(3)
    privince = ""
    city = ""
    if 'privince' in request.POST:
        privince = request.POST['privince']

    if 'city' in request.POST:
        city = request.POST['city']

    area_list =  getAreaList(privince, city)
    if area_list is None:
        area_list = []

    '''
    if "privince" in request.POST:
        a.append(request.POST["privince"])
    '''
    return JsonResponse(area_list)

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
    page = ""

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
    if "page" in request.GET:
        page = request.GET['page']
    # FIXME
    get_rh_list(context, privince, city, area,
            price, bed, str_type, prop, page)

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

def get_type_q_query(str_type):
    if str_type == '1':
        str_type_filter = Q(rh_type__startswith='老年公寓')
    elif str_type == '2':
        str_type_filter = Q(rh_type__startswith='养老照料中心')
    elif str_type == '3':
        str_type_filter = Q(rh_type__startswith='护理院')
    elif str_type == '4':
        str_type_filter = Q(rh_type__startswith='其他')
    else:
        # FIXME
        str_type_filter = None
    return str_type_filter

def get_prop_q_query(prop):
    if prop == '1':
        prop_filter = Q(rh_factory_property__startswith='国营机构')
    elif prop == '2':
        prop_filter = Q(rh_factory_property__startswith='民营机构')
    elif prop == '3':
        prop_filter = Q(rh_factory_property__startswith='公办民营')
    elif prop == '4':
        prop_filter = Q(rh_factory_property__startswith='其他')
    else:
        # FIXME
        prop_filter = None
    return prop_filter

def get_rh_list(context, privince, city, area,
        price, bed, str_type, prop, page):
    global rh_num_per_page
    # FIXME, should not query all DB
    # db = rh.objects.filter(Q(rh_area__endswith="门头沟区"))
    all_filter = Q(rh_area__endswith="海淀区")

    if len(price) != 0 and price != '0':
        price_filter = get_price_q_query(price)
        all_filter = all_filter & price_filter

    if len(bed) != 0 and bed != '0':
        bednum_filter = get_bednum_q_query(bed)
        all_filter = all_filter & bednum_filter

    if len(str_type) != 0 and str_type != '0':
        str_type_filter = get_type_q_query(str_type)
        all_filter = all_filter & str_type_filter

    if len(prop) != 0 and prop != '0':
        prop_filter = get_prop_q_query(prop)
        all_filter = all_filter & prop_filter

    records = rh.objects.filter(all_filter)
    page_num = len(records) / rh_num_per_page
    if len(records) % rh_num_per_page > 0:
        page_num = page_num + 1

    if len(page) == 0 or page == '0':
        page_idx = 1
    else:
        page_idx = int(page)

    ret_records = []
    for idx, r in enumerate(records):
        if idx >= (page_idx - 1) * rh_num_per_page and idx < page_idx * rh_num_per_page:
            found = False
            if len(r.rh_title_image) > 0:
                r.rh_title_image = "title/" + r.rh_title_image
                found = True
            else:
                if len(r.rh_images) > 0:
                    first_img = r.rh_images.split(',')
                    if len(first_img) > 0:
                        r.rh_title_image = first_img[0]
                        found = True
            if found:
                r.rh_title_image = ("/static/images/%d/%s" % (r.id, r.rh_title_image))
            else:
                r.rh_title_image = "/static/images/default.jpg"
            ret_records.append(r)

    context['records'] = ret_records
    context['page_num'] = page_num
    context['curr_page'] = str(page_idx)

    if len(price) == 0:
        context['curr_price'] = '0'
    else:
        context['curr_price'] = price

    if len(bed) == 0:
        context['curr_bednum'] = '0'
    else:
        context['curr_bednum'] = bed

    if len(str_type) == 0:
        context['curr_type'] = '0'
    else:
        context['curr_type'] = str_type

    if len(prop) == 0:
        context['curr_prop'] = '0'
    else:
        context['curr_prop'] = prop

    context['message'] = "privince: " + privince
    context['message'] = context['message'] + ", page_idx: "+ str(page_idx)
    context['message'] = context['message'] + ", page_num: "+ str(page_num)
    context['message'] = context['message'] + ", records_num: "+ str(len(records))
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
