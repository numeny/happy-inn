#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")
sys.path.append("./")

# CGI处理模块
import cgi, cgitb
import MySQLdb as mdb

from db.sql import RhSql

if len(sys.argv) > 1 and len(sys.argv[1]) != 0:
    rh_ylw_id = sys.argv[1]
else:
    # 创建 FieldStorage 的实例化
    form = cgi.FieldStorage() 
    # 获取数据
    rh_ylw_id = form.getvalue('id')

print "Content-type:text/html"
print
print '<html>'
print '<head>'
print '<title>Hello</title>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
print '<title>Example website</title>'
print '</head>'
print '<body>'
print '<h2>Hello Word! This is my first CGI program</h2>'
print '<div>'

print("===================")
print("rh_ylw_id: %s" % rh_ylw_id)
print("===================")
sql = RhSql()
rec = sql.select_one_rh_ylw_id(rh_ylw_id)
if rec == None or len(rec) == 0:
    print('<br />')
    print('<br />')
    print('<b> rh_id: %s not existed!</b>' % rh_ylw_id)
    exit(1)
key_list = (
    "rh_id",
    "rh_name",
    "rh_phone",
    "rh_mobile",
    "rh_email",
    "rh_postcode",
    "rh_location_id",
    "rh_type",
    "rh_factory_property",
    "rh_person_in_charge",
    "rh_establishment_time",
    "rh_floor_surface",
    "rh_building_area",
    "rh_bednum",
    "rh_staff_num",
    "rh_for_persons",
    "rh_charges_extent",
    "rh_special_services",
    "rh_contact_person",
    "rh_address",
    "rh_url",
    "rh_transportation",
    "rh_inst_intro",
    "rh_inst_charge",
    "rh_facilities",
    "rh_service_content",
    "rh_inst_notes",
    "rh_ylw_id",
)
key_list_page = (
    "rh_id",
    "rh_name",
    "rh_establishment_time",
    "rh_bednum",
    "rh_floor_surface",
    "rh_building_area",
    "rh_for_persons",
    "rh_charges_extent",
    "rh_staff_num",
    "rh_type",
    "rh_factory_property",
    "rh_person_in_charge",
    "rh_contact_person",
    "rh_location_id",
    "rh_phone",
    "rh_mobile",
    "rh_email",
    "rh_postcode",
    "rh_url",
    "rh_address",
    "rh_inst_intro",
    "rh_facilities",
    "rh_special_services",
    "rh_service_content",
    "rh_inst_notes",
    "rh_inst_charge",
    "rh_transportation",
    "rh_ylw_id",
)
for row in rec:
    for val_1 in key_list_page:
        for idx, val_2 in enumerate(key_list):
            if not cmp(val_1, val_2):
                break
        print('<p><bold>%s: </bold>' % val_2)
        print(row[idx])
        print('</p>')

print '</div>'
print '</body>'
print '</html>'
