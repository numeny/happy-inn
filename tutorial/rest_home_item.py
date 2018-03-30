#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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
    rh_facilities = scrapy.Field()
    rh_service_content = scrapy.Field()
    rh_inst_notes = scrapy.Field()

    item_list = {
        "rh_name": "unknow resthome name",\
        "rh_phone": "",\
        "rh_location_id": 0,\
        "rh_type": "",\
        "rh_factory_property": "",\
        "rh_person_in_charge": "",\
        "rh_establishment_time": "19990101",\
        "rh_floor_surface": "",\
        "rh_building_area": "",\
        "rh_bednum": 0,\
        "rh_for_persons": "",\
        "rh_charges_extent": "",\
        "rh_special_services": "",\
        "rh_contact_person": "",\
        "rh_address": "",\
        "rh_url": "",\
        "rh_transportation": "",\
        "rh_inst_intro": "",\
        "rh_facilities": "",\
        "rh_service_content": "",\
        "rh_inst_notes": ""\
    }

    def init_item_field_to_default_if_null(item):
        for i in RestHomeItem.item_list:
            if i not in item:
                item[i] = RestHomeItem.item_list[i]
                print("[Warnning] (%s) not existed!" % i)
        item["rh_establishment_time"] = "19790101"
        item["rh_location_id"]=200
        item["rh_bednum"] = 200
        '''
        try:
            item["rh_name"] = item["rh_name"].encode('UTF-8')
            item["rh_phone"] = item["rh_phone"].encode('UTF-8')
            item["rh_type"] = item["rh_type"].encode('UTF-8')
            item["rh_factory_property"] = item["rh_factory_property"].encode('UTF-8')
            item["rh_person_in_charge"] = item["rh_person_in_charge"].encode('UTF-8')
            item["rh_floor_surface"] = item["rh_floor_surface"].encode('UTF-8')
            item["rh_building_area"] = item["rh_building_area"].encode('UTF-8')
            item["rh_for_persons"] = item["rh_for_persons"].encode('UTF-8')
            item["rh_charges_extent"] = item["rh_charges_extent"].encode('UTF-8')
            item["rh_special_services"] = item["rh_special_services"].encode('UTF-8')
            item["rh_contact_person"] = item["rh_contact_person"].encode('UTF-8')
            item["rh_address"] = item["rh_address"].encode('UTF-8')
            item["rh_url"] = item["rh_url"].encode('UTF-8')
            item["rh_transportation"] = item["rh_transportation"].encode('UTF-8')
            item["rh_inst_intro"] = item["rh_inst_intro"].encode('UTF-8')
            item["rh_facilities"] = item["rh_facilities"].encode('UTF-8')
            item["rh_service_content"] = item["rh_service_content"].encode('UTF-8')
            item["rh_inst_notes"] = item["rh_inst_notes"].encode('UTF-8')
        except Exception as e:
            print("*********************************")
            print(e)

        '''
        item["rh_name"] = "海南省托老院"
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
        item["rh_facilities"] = "rh_facilities_5"
        item["rh_service_content"] = "rh_service_content_5"
        item["rh_inst_notes"] = "rh_inst_notes"

    def printSelf(item):
        for i in RestHomeItem.item_list.keys():
            if i in item:
                print("%s: %s" % (i, item[i]))
