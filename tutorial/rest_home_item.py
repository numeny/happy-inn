#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
    def printSelf(item):
        for i in RestHomeItem.item_list.keys():
            if i in item:
                print("{}: {}".format(i, item[i]))
