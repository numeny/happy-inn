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

project_dir = os.environ['HAPPY_INN_PROJECT_PATH'] + "/"

src_root_dir = project_dir + "data.bak/"
src_ylxxw_dir = "picture.ylxxw/"
src_ylw_dir = "picture.ylw/"
dst_root_dir = project_dir + "server/static/images/"

records = models.rh.objects.all()
#records = models.rh.objects.filter(Q(rh_ylw_id__startswith="ff"))
#print len(records)
for r in records:
    '''
    '''
    # search img from rh_ylw_id
    title_image = ""
    print("%d is start" % r.id)
    if r.rh_ylw_id.startswith("ff"):
        rh_ylw_id_pic_dir = src_ylxxw_dir + r.rh_ylw_id[r.rh_ylw_id.find('/') + 1:]
    else:
        rh_ylw_id_pic_dir = src_ylw_dir + r.rh_ylw_id

    if not os.path.exists(src_root_dir + rh_ylw_id_pic_dir):
        print("%d ( %s ) no images" % (r.id, r.rh_ylw_id))
        continue;
    if not os.path.exists(dst_root_dir + str(r.id)):
        os.mkdir(dst_root_dir + str(r.id))
    cp_cmd = "cp -ra " + src_root_dir + rh_ylw_id_pic_dir + "/* " + dst_root_dir + str(r.id);
    os.system(cp_cmd)

    title_dir = dst_root_dir + str(r.id) + "/title"
    if os.path.exists(title_dir):
        files = os.listdir(title_dir)
        if len(files) > 0:
            r.rh_title_image = files[0]
    images_files = os.listdir(dst_root_dir + str(r.id))
    str_all_images = ""
    for f in images_files:
        if f == "title" or f.endswith('/'):
            continue;
        str_all_images = str_all_images + f + ","
    r.rh_images = str_all_images
    r.save()
    print("%d is OK" % r.id)
