#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

class RestHomeItem(scrapy.Item):
    rh_name = scrapy.Field()
    rh_phone = scrapy.Field()

    rh_location_id = scrapy.Field()
    rh_type = scrapy.Field()
    rh_factory_property = scrapy.Field()
    rh_person_in_charge = scrapy.Field()
    rh_establishment_time = scrapy.Field()
    rh_floor_surface = scrapy.Field()
    rh_building_area = scrapy.Field()
    rh_bednum = scrapy.Field()
    rh_for_persons = scrapy.Field()
    rh_charges_extent = scrapy.Field()
    rh_special_services = scrapy.Field()

    rh_contact_person = scrapy.Field()
    rh_address = scrapy.Field()
    rh_url = scrapy.Field()
    rh_transportation = scrapy.Field()

    rh_inst_intro = scrapy.Field()
    rh_inst_charge = scrapy.Field()
    rh_facilities = scrapy.Field()
    rh_service_content = scrapy.Field()
    rh_inst_notes = scrapy.Field()

    item_list = (
        ("rh_name", "unknow resthome name"),\
        ("rh_phone", ""),\
        ("rh_location_id", ""),\
        ("rh_type", ""),\
        ("rh_factory_property", ""),\
        ("rh_person_in_charge", ""),\
        ("rh_establishment_time", u"1999年01月01日"),\
        ("rh_floor_surface", ""),\
        ("rh_building_area", ""),\
        ("rh_bednum", u"0张"),\
        ("rh_for_persons", ""),\
        ("rh_charges_extent", ""),\
        ("rh_special_services", ""),\
        ("rh_contact_person", ""),\
        ("rh_address", ""),\
        ("rh_url", ""),\
        ("rh_transportation", ""),\
        ("rh_inst_intro", ""),\
        ("rh_inst_charge", ""),\
        ("rh_facilities", ""),\
        ("rh_service_content", ""),\
        ("rh_inst_notes", "")\
    )

    def init_item_field_to_default_if_null(item):
        for i in RestHomeItem.item_list:
            if i[0] not in item:
                item[i[0]] = i[1]
                print("[Warning] (%s) not existed!" % i[0])
        RestHomeItem.handleString(item, "rh_name");
        RestHomeItem.handleString(item, "rh_phone");
        RestHomeItem.handleString(item, "rh_location_id");
        RestHomeItem.handleString(item, "rh_type");
        RestHomeItem.handleString(item, "rh_factory_property");
        RestHomeItem.handleString(item, "rh_person_in_charge");
        RestHomeItem.handleString(item, "rh_floor_surface");
        RestHomeItem.handleString(item, "rh_building_area");
        RestHomeItem.handleString(item, "rh_for_persons");
        RestHomeItem.handleString(item, "rh_charges_extent");
        RestHomeItem.handleString(item, "rh_special_services");
        RestHomeItem.handleString(item, "rh_contact_person");
        RestHomeItem.handleString(item, "rh_address");
        RestHomeItem.handleString(item, "rh_url");
        RestHomeItem.handleString(item, "rh_transportation");
        RestHomeItem.handleString(item, "rh_inst_intro");
        RestHomeItem.handleString(item, "rh_inst_charge");
        RestHomeItem.handleString(item, "rh_facilities");
        RestHomeItem.handleString(item, "rh_service_content");
        RestHomeItem.handleString(item, "rh_inst_notes");

        RestHomeItem.handleDate(item, "rh_establishment_time")
        RestHomeItem.handleOneNum(item, "rh_bednum")

        '''

        item["rh_name"] = "海南省托老"
        item["rh_phone"] = "rh_phone_6"
        item["rh_type"] = "rh_type_5"
        item["rh_factory_property"] = "rh_factory_property_5"
        item["rh_person_in_charge"] = "rh_person_in_charge_5"
        item["rh_floor_surface"] = "rh_floor_surface_5"
        item["rh_building_area"] = "rh_building_area_5"
        item["rh_for_persons"] = "rh_for_persons_5"
        item["rh_charges_extent"] = "rh_charges_extent_5"
        item["rh_special_services"] = "rh_special_services_5"
        item["rh_contact_person"] = "rh_contact_person_5"
        item["rh_address"] = "rh_address_5"
        item["rh_url"] = "rh_url_5"
        item["rh_transportation"] = "rh_transportation_5"
        item["rh_inst_intro"] = "rh_inst_intro_5"
        item["rh_inst_charge"] = "rh_inst_charge_5"
        item["rh_facilities"] = "rh_facilities_5"
        item["rh_service_content"] = "rh_service_content_5"
        item["rh_inst_notes"] = "rh_inst_notes"
        '''
    def handleString(item, idx):
        try:
            item[idx] = item[idx].encode('UTF-8')
        except Exception as e:
            print("*********************************")
            print(e)

    def handleDate(item, idx):
        ''' item.[idx] is u"1999年1月11日" '''
        item[idx] = item[idx].strip()
        old_item = item[idx]
        pattern = re.compile(r'[^\d]')
        m = pattern.split(item[idx])
        if(len(m) < 2):
            print("[Error-parse]: rh_establishment_time is not correct, for %s" % item["rh_url"])
            print(item[idx])
            return
        item[idx] = "{:0>4s}{:0>2s}{:0>2s}".format(m[0].encode('utf-8'), m[1].encode('utf-8'), m[2].encode('utf-8'))
        if len(old_item) != 0 and len(item[idx]) == 0:
            print("[Error-parse]: %s is not correct, for %s, item[%s]: %s" % (idx, item["rh_url"], idx, old_item))

    def handleOneNum(item, idx):
        # item.[idx] is u"汉字num汉字"
        item[idx] = item[idx].strip()
        old_item = item[idx]
        pattern = re.compile(r'[^\d]')
        m = pattern.split(item[idx])
        item[idx] = int(m[0].encode('utf-8'))
        if len(old_item) != 0 and item[idx] == 0:
            print("[Error-parse]: %s is not correct, for %s, item[%s]: %s" % (idx, item["rh_url"], idx, old_item))

    def printSelf(item):
        for i in RestHomeItem.item_list:
            if i[0] in item:
                print("%s: %s" % (i[0], item[i[0]]))
            else:
                print("%s: not in item" % (i[0]))
