#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import sys

import scrapy
import re

sys.path.append("../")

from utils import my_log

logger = my_log.get_my_logger()

class RestHomeItem(scrapy.Item):
    rh_name = scrapy.Field()
    rh_phone = scrapy.Field()
    rh_mobile = scrapy.Field()
    rh_email = scrapy.Field()
    rh_postcode = scrapy.Field()

    rh_location_id = scrapy.Field()
    rh_type = scrapy.Field()
    rh_factory_property = scrapy.Field()
    rh_person_in_charge = scrapy.Field()
    rh_establishment_time = scrapy.Field()
    rh_floor_surface = scrapy.Field()
    rh_building_area = scrapy.Field()
    rh_bednum = scrapy.Field()
    rh_staff_num = scrapy.Field()
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

    rh_ylw_id = scrapy.Field()

    item_list = (
        ("rh_name", "unknow resthome name"),\
        ("rh_phone", ""),\
        ("rh_mobile", ""),\
        ("rh_email", ""),\
        ("rh_postcode", ""),\
        ("rh_location_id", ""),\
        ("rh_type", ""),\
        ("rh_factory_property", ""),\
        ("rh_person_in_charge", ""),\
        ("rh_establishment_time", u""),\
        ("rh_floor_surface", ""),\
        ("rh_building_area", ""),\
        ("rh_bednum", ""),\
        ("rh_staff_num", ""),\
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
        ("rh_inst_notes", ""),\
        ("rh_ylw_id", "")\
    )

    @staticmethod
    def init_item_field_to_default_if_null(item):
        try:
            for i in RestHomeItem.item_list:
                if i[0] not in item:
                    item[i[0]] = i[1]
                    logger.warning("(%s) not existed!" % i[0])
            RestHomeItem.handleString(item, "rh_name");
            RestHomeItem.handleString(item, "rh_phone");
            RestHomeItem.handleString(item, "rh_mobile");
            RestHomeItem.handleString(item, "rh_email");
            RestHomeItem.handleString(item, "rh_postcode");
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
            RestHomeItem.handleString(item, "rh_ylw_id");

            RestHomeItem.handleString(item, "rh_establishment_time")
            RestHomeItem.handleString(item, "rh_bednum")
            RestHomeItem.handleString(item, "rh_staff_num")
        except Exception as e:
            logger.critical("Error: init_item_field_to_default_if_null(), for rh_ylw_id: %s" % item['rh_ylw_id'])
            logger.critical(e)


    def handleString(item, idx):
        try:
            # change " to \"
            item[idx] = item[idx].replace('\"', '\\\"').encode('UTF-8')
        except Exception as e:
            logger.warning("handleString() error when handle item: %s, value: %s" % (idx, item[idx]))
            logger.warning(e)

    def handleDate(item, idx):
        ''' item.[idx] is u"1999年1月11日" or u"1999年1月" or u"1999年"'''
        item[idx] = item[idx].strip()
        old_item = item[idx]
        pattern = re.compile(r'[^\d]')
        m = pattern.split(item[idx])
        if len(m) == 0:
            logger.error("rh_establishment_time is not correct, for %s" % item["rh_ylw_id"])
            logger.error(item[idx])
            return
        if len(m[0]) == 0:
            m[0] = u"1999"
        if (len(m) <= 1 or len(m[1])) == 0:
            m[1] = u"01"
        if (len(m) <= 2 or len(m[2])) == 0:
            m[2] = u"01"
        item[idx] = "{:0>4s}{:0>2s}{:0>2s}".format(m[0].encode('utf-8'), m[1].encode('utf-8'), m[2].encode('utf-8'))
        if len(old_item) != 0 and len(item[idx]) == 0:
            logger.error("[Error-parse]: %s is not correct, for %s, item[%s]: %s" % (idx, item["rh_url"], idx, old_item))

    def handleOneNum(item, idx):
        # item.[idx] is u"汉字num汉字"
        item[idx] = item[idx].strip()
        old_item = item[idx]
        pattern = re.compile(r'[^\d]')
        m = pattern.split(item[idx])
        item[idx] = int(m[0].encode('utf-8'))
        if len(old_item) != 0 and item[idx] == 0:
            logger.warning("[Error-parse]: %s is not correct, for %s, item[%s]: %s" % (idx, item["rh_url"], idx, old_item))

    @staticmethod
    def getFirstNum(s):
        pattern = re.compile(r'[^\d]')
        m = pattern.split(s)
        return m[0].encode('utf-8')

    @staticmethod
    def printSelf(item):
        for i in RestHomeItem.item_list:
            if i[0] in item:
                logger.debug("%s: %s" % (i[0], item[i[0]]))
            else:
                logger.warning("%s: not in item" % (i[0]))

    @staticmethod
    def printOneRecord(record):
        if record is None:
            return
        logger.debug("rh_id: %s" % record[0])
        idx = 1
        for i in RestHomeItem.item_list:
            print("%s: %s" % (i[0], record[idx]))
            idx = idx + 1
        print("")
