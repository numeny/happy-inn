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
#print len(records)
for r in records:
    '''
    '''
    rh_bednum = r.rh_bednum.encode('utf-8').replace("张", "").replace("-", "0")

    rh_charges_extent = r.rh_charges_extent.encode('utf-8').replace("元", "").replace("--", "-");
    idxLine = rh_charges_extent.find('-');
    len_rh_charges_extent = len(rh_charges_extent)
    if idxLine == -1:
        print("Error: rh_charges_extent can't find char(-), for rh_ylw_id: %s, rh_charges_extent: %s" % (r.rh_ylw_id, r.rh_charges_extent))
        continue;
    if idxLine == 0:
        chargesMin = ""
    elif idxLine > 0:
        chargesMin = rh_charges_extent[0 : idxLine]

    if idxLine == (len_rh_charges_extent - 1):
        chargesMax = ""
    else:
        chargesMax = rh_charges_extent[idxLine + 1 : ]

    chargesMin = chargesMin.strip()
    chargesMax = chargesMax.strip()

    if len(chargesMin) == 0:
        chargesMin = 0
    elif chargesMin.isdigit():
        chargesMin = int(chargesMin)
    else:
        print("Error: rh_charges_extent minimum is unormal, for rh_ylw_id: %s, rh_charges_extent: %s" % (r.rh_ylw_id, r.rh_charges_extent))
        continue;

    if len(chargesMax) == 0:
        chargesMax = 1000000
    elif chargesMax.isdigit():
        chargesMax = int(chargesMax)
    else:
        print("Error: rh_charges_extent maxmum is unormal, for rh_ylw_id: %s, rh_charges_extent: %s" % (r.rh_ylw_id, r.rh_charges_extent))
        continue;
    print("[%d %d]                    rh_ylw_id: %s[%s]" % (chargesMin, chargesMax, r.rh_ylw_id.encode('utf-8'), r.rh_charges_extent.encode('utf-8')));
    r.rh_charges_min = chargesMin
    r.rh_charges_max = chargesMax

    if r.rh_ylw_id.startswith("ff"):
        rh_prop = r.rh_factory_property
        rh_type = r.rh_type

        if len(rh_prop) == 0 or rh_prop == '-':
            print("rh_ylw_id: %s[%s]" % (r.rh_ylw_id.encode('utf-8'), rh_prop.encode('utf-8')));
            rh_prop = "其他"
        if len(rh_type) == 0 or rh_type == '-':
            print("rh_ylw_id: %s[%s]" % (r.rh_ylw_id.encode('utf-8'), rh_type.encode('utf-8')));
            rh_type = "其他"

        r.rh_factory_property = rh_type
        r.rh_type = rh_prop

    r.save()
