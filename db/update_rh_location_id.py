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

records = models.rh.objects.all()

#records = models.rh.objects.filter(Q(rh_ylw_id__startswith="ff"))
for r in records:
    '''
    '''
    existedRecords = models.city.objects.filter(privince=r.rh_privince, city=r.rh_city, area=r.rh_area)
    if len(existedRecords) == 0:
        print("not existed and insert to city'db for [%s] [%s] [%s] " % (r['rh_privince'].encode('utf8'), r['rh_city'].encode('utf8'), r['rh_area'].encode('utf8')))
        models.city.objects.create(privince=r['rh_privince'].encode('utf8'), city=r['rh_city'].encode('utf8'), area=r['rh_area'].encode('utf8'))
        continue;
    if len(existedRecords) > 1:
        print("existed exceed 1 record for city'db for [%s] [%s] [%s] " % (r['rh_privince'].encode('utf8'), r['rh_city'].encode('utf8'), r['rh_area'].encode('utf8')))
        continue;
    print("area id: %d" % existedRecords[0].id)
    r.rh_location_id = str(existedRecords[0].id)
    r.save()
