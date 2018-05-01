#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, re

sys.path.append('../server/')
os.environ['DJANGO_SETTINGS_MODULE'] ='server.settings'

from server import settings
import django

django.setup()

from rh import models
from django.db.models import Q

rh_cities = models.rh.objects.order_by('rh_privince', 'rh_city', 'rh_area').values('rh_privince', 'rh_city', 'rh_area').distinct()
#records = models.rh.objects.filter(Q(rh_ylw_id__startswith="ff"))
for r in rh_cities:
    '''
    '''
    existedRecords = models.city.objects.filter(privince=r['rh_privince'], city=r['rh_city'], area=r['rh_area'])
    if len(existedRecords) > 0:
        print("existed for [%s] [%s] [%s] " % (r['rh_privince'].encode('utf8'), r['rh_city'].encode('utf8'), r['rh_area'].encode('utf8')))
        continue;
    models.city.objects.create(privince=r['rh_privince'].encode('utf8'), city=r['rh_city'].encode('utf8'), area=r['rh_area'].encode('utf8'))
