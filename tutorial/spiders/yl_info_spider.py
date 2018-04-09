#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import scrapy
import logging
from scrapy import Selector

sys.path.append("../../")

from utils import my_log
from utils import file_util

from tutorial.rest_home_item import RestHomeItem

total_idx = 0
logger = my_log.get_my_logger()

class YLInfoRestHomeSpider(scrapy.Spider):
    name = "YLInfoRestHome"
    __host_pc = "http://www.yanglaocn.com"
    __host_mobile = "http://m.yanglaocn.com"

    __pic_root_path = os.path.join("result", "picture")


    def start_requests(self):
        logger.debug("start_requests ...")
        file_util.create_dir(self.__pic_root_path)
        urls = [
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=0',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=022',
            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=0955',
#            'http://m.yanglaocn.com/shtml/ylyxx/2016-04/yly146172868824614.html'
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=02201&page=2',
#            'http://www.yanglaocn.com/yanglaoyuan/yly',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=01001&gotoip=y',
#            'http://m.yanglaocn.com/shtml/ylyxx/2014-06/yly140411449322841.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_idx
        logger.info("starting parse() ... response: %s" % response.url)
        '''
        title_str = "RgSelect="
        pos_title_str = response.url.find(title_str)
        if pos_title_str != -1:
            area_url_start_idx = pos_title_str + len(title_str)
            area_url = response.url[area_url_start_idx: len(response.url)]
            if len(area_url) <= 1: #avoid parsing the area's page of one privince
                logger.debug(" starting parse privince list ... area_url: %s" % area_url)
                # all province
                # get all url of privice's resthome list
                privince_url_list = response.xpath('//div[@class="querywhere"]/div[@class="sanxiantj"]/div[@class="jigouquyu_right"]/label/a/@href').extract()
                for privince_url in privince_url_list:
                    logger.info("send request for privince_url: %s" % privince_url)
                    yield scrapy.Request(url=privince_url, callback=self.parse)
        '''
        '''
        # get next page of rest home list
        anchor_list_next_page_in_privince = response.xpath('//div[@class="main"]/div[@class="page"]/div[@class="webpage"]/a').extract()
        for x in anchor_list_next_page_in_privince:
            logger.debug("starting parse : rest home list for next page of one privince ...")
            m = Selector(text=x).xpath("//a/span/text()").extract()
            str_next_page = u'\u4e0b\u4e00\u9875' # next_page
            if len(m) > 0 and not cmp(str_next_page, m[0]):
                n = Selector(text=x).xpath("//a/@href").extract()
                if len(n) > 0:
                    url_next_page = response.url[:response.url.rfind('/')] + n[0]
                    logger.info("starting parse : rest home list for next page of one privince ... %s" % url_next_page)
                    yield scrapy.Request(url=url_next_page, callback=self.parse)

        '''

        # all url for one province's one page
        url_list_in_privince_one_page = response.xpath('//div[@class="querywhere2"]/div[@class="jiadiantucontext"]/div[@class="jiadiantucontext_ul"]/a/@href').extract()
        for u in url_list_in_privince_one_page:
            u = u.replace("www", "m")
            logger.info("starting parse : start request for url request for one mobile website ... %s" % u)
            yield scrapy.Request(url=u, callback=self.parse_page)

#        self.parse_page(response)

    def parse_page(self, response):
#        self.parse_picture_1(response)
        logger.info("starting parse one mobile page ... %s" % response.url)
        pos = response.url.find("ylyxx")
        if pos == -1:
            logger.error("parse rh_ylw_id error ... %s, can't find str \"ylyxx\" in url" % response.url)
            pos = 0
        rh_ylw_id = "ff-" + response.url[pos + len("ylyxx") + 1:]
        rh_ylw_id = rh_ylw_id.replace(".html", "")

        len1 = rh_ylw_id.rfind("/")
        if len1 == -1:
            logger.error("parse rh_ylw_id error ... %s" % response.url)
        len2 = len(rh_ylw_id)
        rh_ylw_id_for_pic = rh_ylw_id[len1+1:len2]

        logger.info("start picture request for ... rh_ylw_id: %s" % rh_ylw_id_for_pic)
        # normal picture
        url_list = response.xpath('//div[@id="pic_ylyxx"]/img/@src').extract()
        for url in url_list:
            if len(url) > 0 and url.startswith("http"):
                yield scrapy.Request(url=url, callback=self.save_normal_pic, meta={"rh_ylw_id": rh_ylw_id_for_pic})
                pass
        # title picture
        url_list = response.xpath('//div[@class="mymain"]/div[@class="navTitle"]/span/img/@src').extract()
        for url in url_list:
            if len(url) > 0 and url.startswith("http"):
                yield scrapy.Request(url=url, callback=self.save_title_pic, meta={"rh_ylw_id": rh_ylw_id_for_pic})
                pass

        yield self.parse_item_from_response(response)

    def parse_item_from_response(self, response):
        logger.info("parse item start ... %s" % response.url)

        rhit = RestHomeItem()

        logger.debug("\nparsing basicInformation ...\n")
        # basicInformation
        self.fill_item_with_list(rhit, response)
        rh_name = response.xpath('//div[@id="BasicInformation"]/div[@class="leftcontexttitle"]/label/text()').extract()
        if len(rh_name) > 0:
            rhit['rh_name'] = rh_name[0]

        # Contact US info
        logger.debug("\nparsing ContactUsList ...\n")
        self.fill_item_with_list(rhit, response)
        rh_url = response.xpath('//div[@id="ContactUsList"]/div[@class="leftcontexttitle"]/a/@href').extract()
        if len(rh_url) > 0:
            rhit['rh_url'] = rh_url[0]
        if 'rh_contact_person' in rhit:
            rhit['rh_person_in_charge'] = rhit['rh_contact_person']

        # OrganizationsOn_Text etc.
        logger.debug("\nparsing OrganizationsOn etc ...\n")
        self.fill_item_with_p_lable_list(rhit, response)

        # for exam: m.yanglaocn.com/shtml/ylyxx/2013-04/yly1365591790411.html
        rhit['rh_ylw_id'] = "ff-" + response.url[response.url.find("ylyxx") + len("ylyxx") + 1:]
        rhit['rh_ylw_id'] = rhit['rh_ylw_id'].replace(".html", "")

        RestHomeItem.printSelf(rhit)
        return rhit

    def fill_item_with_list(self, rhit, response):
        logger.debug("start fill_item_with_list ...")
        item_list = (
            ('BasicInformation',
                ('rh_establishment_time',
                 'rh_bednum',
                 'rh_floor_surface',
                 'rh_for_persons',
                 'rh_charges_extent',
                 'rh_staff_num',
                 'rh_type',
                 'rh_factory_property'),
            ),
            ('ContactUsList',
                ('rh_contact_person',
                 'rh_location_id',
                 'rh_phone',
                 'rh_mobile',
                 'rh_email',
                 'rh_postcode',
                 'rh_address'),
             ),)

        for i in item_list:
            str_xpath = '//div[@id="' + i[0] + '"]/div[@class="leftcontexttitle"]/text()'
            leftcontexttitle_list = response.xpath(str_xpath).extract()
            logger.debug("start parsing lefttitle -1")
            for idx, val in enumerate(i[1]):
                logger.debug("start parsing lefttitle -2: %s" % val)
                if len(leftcontexttitle_list) > idx and len(leftcontexttitle_list[idx].strip()) > 0:
                    rhit[val] = leftcontexttitle_list[idx].strip()
                    logger.debug("start parsing lefttitle -3: %s" % rhit[val])


    def fill_item_with_p_lable_list(self, rhit, response):
        logger.debug("start fill_item_with_p_lable_list 0 ...")
        item_list = (
            ("OrganizationsOn_Text", "rh_inst_intro"),
            ("EnvironmentalFacilities_Text", "rh_facilities"),
            ("DietaryIntroduced_Text","rh_service_content"),
            ("CheckinNotes_Text","rh_inst_notes"),
            ("FeeScale_Text","rh_inst_charge"),
            ("TrafficInformation_Text","rh_transportation"),
        )
        for i in item_list:
            str_xpath = '//div[@id="' + i[0] + '"]/p'
            info = response.xpath(str_xpath).extract()
            str_info = ""
            for j in info:
                str_info = str_info + j
            if len(str_info) > 0:
                rhit[i[1]] = str_info

    def save_normal_pic(self, response):
        logger.debug("save_normal_pic ... ")
        self.save_pic(response, False)
        pass

    def save_title_pic(self, response):
        logger.debug("save_title_pic ... ")
        self.save_pic(response, True)

    def save_pic(self, response, is_title):
        file_name = response.url[(response.url.rfind("/") + 1) : ];
        resthome_id = response.meta["rh_ylw_id"]
        picture_dir = os.path.join(self.__pic_root_path, resthome_id)

        file_util.save_pic(picture_dir, file_name, is_title, response.body)
