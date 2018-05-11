#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, re

sys.path.append('../server/')
sys.path.append('server/')

os.environ['DJANGO_SETTINGS_MODULE'] ='server.settings'

from server import settings
import django

django.setup()

from rh import models
from django.db.models import Q

#records = models.rh.objects.all()
records = models.rh.objects.filter(~Q(rh_ylw_id__startswith="ff") and Q(rh_phone__startswith="login"))
#print len(records)
for r in records:
    '''
    '''
    # search img from rh_ylw_id
    record2 = models.rh.objects.filter(Q(rh_name__startswith=r.rh_name) and Q(rh_ylw_id__startswith="ff"))
    print('process %s: %s' % (r.rh_ylw_id.encode('utf-8'), r.rh_name.encode('utf-8')))
    if record2.count() == 0 and record2[0].rh_phone.length == 0:
        continue;
    r.rh_phone = record2[0].rh_phone
    r.save()
    print("%d is OK" % r.id)
