#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql
from db.city_sql import CitySql

static_sql_str = "update rh set \
            rh_privince=\"%s\", \
            rh_city=\"%s\", \
            rh_area=\"%s\" \
            where rh_id=%d;"


test_RhSql = RhSql()
city_sql = CitySql()

results = test_RhSql.select_all()

def updateDb(rh_id, privince, city, area):
    global sql_str
    rh_privince = privince
    rh_city = city
    rh_area = area

    if privince is None:
        rh_privince = ""
    if city is None:
        rh_city = ""
    if area is None:
        rh_area = ""
    sql_str = static_sql_str
    sql_str = sql_str % (rh_privince.encode("utf-8"), rh_city.encode("utf-8"), rh_area.encode("utf-8"), rh_id)
    try:
        test_RhSql.excute_sql(sql_str)
    except Exception as e:
        print("Error excute sql, sql_str: %s" % sql_str)
        print(e)

debug = False
idx = 0
for i in results:
    idx = idx + 1; 
    if idx == 2:
        debug = True
    else:
        debug = True
    if i is None:
        if debug:
            print("no record, sql.py")
        break;
    if debug:
        print("rh_id: %s" % i[0])
    rh_id = i[0]
    rh_location_id = i[6]
    city_results = city_sql.select_all()
    found = False
    for j in city_results:
        priv = j[1].decode()
        city = j[2].decode()
        area = j[3].decode()
        if priv.endswith("自治区"):
            priv_end = 2;
        else:
            priv_end = len(priv)-1;
        if len(area) <= 2:
            area_end = len(area);
        else:
            area_end = len(area)-1;
        if j is None:
            break;
        if rh_location_id.find(priv[0:priv_end]) != -1 and rh_location_id.find(city[0:len(city)-1]) != -1 and rh_location_id.find(area[0:area_end]) != -1:
            if debug:
                print("rh_area 1: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
            found = True
            updateDb(rh_id, priv, city, area)
            break;

    if found:
        continue;
    else:
        for j in city_results:
            priv = j[1].decode()
            city = j[2].decode()
            area = j[3].decode()
            if priv.endswith("自治区"):
                priv_end = 2;
            else:
                priv_end = len(priv)-1;
            if len(area) <= 2:
                area_end = len(area);
            else:
                area_end = len(area)-1;
            if j is None:
                break;
            if rh_location_id.find(city[0:len(city)-1]) != -1 and rh_location_id.find(area[0:area_end]) != -1:
                if debug:
                    print("rh_area 2: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
                found = True
                updateDb(rh_id, priv, city, area)
                break;

    if found:
        continue;
    else:
        for j in city_results:
            priv = j[1].decode()
            city = j[2].decode()
            area = j[3].decode()
            if priv.endswith("自治区"):
                priv_end = 2;
            else:
                priv_end = len(priv)-1;
            if len(area) <= 2:
                area_end = len(area);
            else:
                area_end = len(area)-1;
            if j is None:
                break;
            if rh_location_id.find(priv[0:priv_end]) != -1 and rh_location_id.find(area[0:area_end]) != -1:
                if debug:
                    print("rh_area 3: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
                found = True
                updateDb(rh_id, priv, city, area)
                break;

    if found:
        continue;
    else:
        for j in city_results:
            priv = j[1].decode()
            city = j[2].decode()
            area = j[3].decode()
            if priv.endswith("自治区"):
                priv_end = 2;
            else:
                priv_end = len(priv)-1;
            if len(area) <= 2:
                area_end = len(area);
            else:
                area_end = len(area)-1;
            if j is None:
                break;
            if rh_location_id.find(priv[0:priv_end]) != -1 and rh_location_id.find(city[0:len(city)-1]) != -1:
                if debug:
                    print("rh_area 4: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
                found = True
                updateDb(rh_id, priv, city, None)
                break;


    if found:
        continue;
    else:
        for j in city_results:
            priv = j[1].decode()
            city = j[2].decode()
            area = j[3].decode()
            if priv.endswith("自治区"):
                priv_end = 2;
            else:
                priv_end = len(priv)-1;
            if j is None:
                break;
            if rh_location_id.find(priv[0:priv_end]) != -1:
                if debug:
                    print("rh_area 5: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
                found = True
                updateDb(rh_id, priv, None, None)
                break;

    if not found:
        print("rh_area 9: [%s %s %s], [%s]" % (j[1], j[2], j[3], i[6]))
            
#@if i[6].find()
    
#test_RhSql.excute_sql(sql_str):
