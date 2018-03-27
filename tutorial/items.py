# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YlyItem(scrapy.Item):
    city = scrapy.Field()
    yly_type = scrapy.Field()
    factory_property = scrapy.Field()
    person_in_charge = scrapy.Field()
    establishment_time = scrapy.Field()
    floor_surface = scrapy.Field()
    building_area = scrapy.Field()
    bednum = scrapy.Field()
    for_persons = scrapy.Field()
    charges_extent = scrapy.Field()
    special_services = scrapy.Field()

    contact_person = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    transportation = scrapy.Field()
