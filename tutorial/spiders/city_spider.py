#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import scrapy
from scrapy import Selector

sys.path.append("../../")

from utils import my_log
from tutorial.city_item import CityItem

logger = my_log.get_my_logger()

total_privinces = 0
total_cities = 0
total_areas = 0

class CityListSpider(scrapy.Spider):
    name = "CityListSpider"

    def start_requests(self):
        '''
        '''
        urls = [
            'http://www.yanglaocn.com/yanglaoyuan/citylist.php',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=099111',
#            'http://www.yanglao.com.cn/resthome/41090.html',
#            'http://www.yanglao.com.cn/resthome/228436.html',
#            'http://www.yanglao.com.cn/xinjiang',
#            'http://www.yanglao.com.cn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_privinces
        global total_cities
        global total_areas

        print("parsing city list's url ... %s" % response.url)

        # get title picture's src and send request
        privinces = response.xpath('//div[@id="InsuAllCity"]/div[@class="insuccententul"]').extract()
        for p in privinces:
            total_privinces = total_privinces + 1
            privince = Selector(text=p).xpath('//div[@class="insuccententlileft"]/a[@class="query"]/text()').extract()
            privince_text_is_null = (len(privince) == 0)
            logger.debug("request privince [%d]" % (total_privinces))
            cities = Selector(text=p).xpath('//div[@class="insuccententliright"]/a[@class="ameth2"]').extract()
            for c in cities:
                city = Selector(text=c).xpath('//a[@class="ameth2"]/span/text()').extract()
                city_url = Selector(text=c).xpath('//a[@class="ameth2"]/@href').extract()
                if len(city) < 1 or len(city_url) < 1:
                    logger.critical("Error: len(city) < 1, for url: %s" % response.url)
                if privince_text_is_null:
                    privince_text = city[0]
                else:
                    privince_text = privince[0]
                total_cities = total_cities + 1
                logger.debug("----- request cities [%d] for prinvice [%s], city[%s]" % (total_cities, privince_text, city[0]))
                yield scrapy.Request(url=city_url[0], callback=self.parse, meta={"privince": privince_text, "city": city[0]})

        areas = response.xpath('//div[@class="querywhere"]/div[@class="sanxiantj"]/div[@class="jigouquyu_right"]/label/a/text()').extract()
        for a in areas:
            p = ""
            c = ""
            if "privince" in response.meta:
                p = response.meta["privince"]
            if "city" in response.meta:
                c = response.meta["city"]
            print("[%s][%s][%s]" % (p, c, a))
            ci = CityItem()
            ci['privince'] = p
            ci['city'] = c
            ci['area'] = a
            total_areas = total_areas + 1
            logger.debug("----- request area [%d] for prinvice [%s], city[%s], area[%s]" % (total_areas, p, c, a))
            yield ci
