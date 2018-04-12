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

class CityItem(scrapy.Item):
    privince = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()

    item_list = (
        ("privince", ""),\
        ("city", ""),\
        ("area", ""),\
    )

    @staticmethod
    def init_item_field_to_default_if_null(item):
        try:
            for i in CityItem.item_list:
                if i[0] not in item:
                    item[i[0]] = i[1]
                    logger.warning("(%s) not existed!" % i[0])
            CityItem.handleString(item, "privince");
            CityItem.handleString(item, "city");
            CityItem.handleString(item, "area");
        except Exception as e:
            logger.critical("Error: init_item_field_to_default_if_null(), for privince: %s" % item['privince'])
            logger.critical(e)


    def handleString(item, idx):
        try:
            # change " to \"
            item[idx] = item[idx].replace('\"', '\\\"').encode('UTF-8')
        except Exception as e:
            logger.warning("handleString() error when handle item: %s, value: %s" % (idx, item[idx]))
            logger.warning(e)

    @staticmethod
    def printSelf(item):
        for i in CityItem.item_list:
            if i[0] in item:
                logger.debug("%s: %s" % (i[0], item[i[0]]))
            else:
                logger.warning("%s: not in item" % (i[0]))

    @staticmethod
    def printOneRecord(record):
        if record is None:
            return
        logger.debug("id: %s" % record[0])
        idx = 1
        for i in CityItem.item_list:
            print("%s: %s" % (i[0], record[idx]))
            idx = idx + 1
        print("")
