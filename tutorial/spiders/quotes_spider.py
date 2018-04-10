#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

import scrapy
import logging
from scrapy import Selector

sys.path.append("../../")

from utils import my_log
from utils import file_util

from tutorial.rest_home_item import RestHomeItem


logger = my_log.get_my_logger()
total_privinces = 0
total_pages = 0
total_idx = 0

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    __pic_root_path = os.path.join("result", "picture")

    def start_requests(self):
        logger.info("start_requests ...")
        file_util.create_dir(self.__pic_root_path)
        urls = [
#            'http://www.yanglao.com.cn/tianjin',
#            'http://www.yanglao.com.cn/resthome/8086.html',
#            'http://www.yanglao.com.cn/resthome/20671.html',
#            'http://www.yanglao.com.cn/resthome/20665.html',
#            'http://www.yanglao.com.cn/resthome/20666.html',
            'http://www.yanglao.com.cn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_privinces
        global total_pages
        global total_idx

        # all province
        # get all url of privice's resthome list
        try:
            '''
            '''
            privince_url_list = response.xpath('//div[@class="hot-items"]/div[@class="hot-cities"]/dl/dd/a/@href').extract()
            for privince_url in privince_url_list:
                privince_url = "http://www.yanglao.com.cn" + privince_url
                total_privinces = total_privinces + 1
                logger.info("====total_privinces: %d===== privince_url: %s" % (total_privinces, privince_url))
                yield scrapy.Request(url=privince_url, callback=self.parse)

            # next pages for one province
            '''
            '''
            # get next page of rest home list
            page_list_in_privince = response.xpath('//div[@class="pager"]/ul[@class="pages"]/li').extract()
            for one_page_li in page_list_in_privince:
                page_list_text = Selector(text=one_page_li).xpath('//li/a/text()').extract()
                for page_url_text in page_list_text:
                    if page_url_text == u'\u4e0b\u4e00\u9875':
                        next_page_urls = Selector(text=one_page_li).xpath('//li/a/@href').extract()
                        for next_page_url in next_page_urls:
                            next_page_abs_url = "http://www.yanglao.com.cn" + next_page_url.strip()
                            total_pages = total_pages + 1
                            logger.info("====total_pages: %d===== next_page_abs_url: %s" % (total_pages, next_page_abs_url))
                            yield scrapy.Request(url=next_page_abs_url, callback=self.parse)

            # all url for one province's one page
            rh_items_in_privince_one_page = response.xpath('//div[@class="restlist"]/div[@class="list-view"]/ul[@class="rest-items"]/li[@class="rest-item"]/div[@class="info"]/h4/a/@href').extract()
            for url in rh_items_in_privince_one_page:
                total_idx = total_idx + 1
                logger.info("====total_idx: %d===== rh_item_url: %s" % (total_idx, url))
                url = "http://www.yanglao.com.cn" + url.strip()
                yield scrapy.Request(url=url, callback=self.parse_one_rh)
        except Exception as e:
            logger.critical("Error: parse(), for url: %s" % response.url)
            logger.critical(e)

    def parse_one_rh(self, response):
        try:
            logger.info("parsing one rest home's page ... url: %s" % response.url)
            # get title picture's src and send request
            title_pictures = response.xpath('//div[@class="inst-info"]/div[@class="cont"]/div[@class="inst-pic"]/img/@src').extract()
            rh_ylw_id_for_pic = self.get_rh_ylw_id(response)
            logger.debug("sending title picture request -00")
            for title_picture in title_pictures:
                logger.debug("sending title picture request -0")
                if len(title_picture) != 0 and cmp(title_picture, "/images/no_image.gif"): # default picture for no image
                    logger.debug("sending title picture request - 1")
                    if title_picture.startswith("http"):
                        logger.debug("sending title picture request - 2")
                        logger.debug("sending title picture request ... %s" % response.url)
                        yield scrapy.Request(url=title_picture, callback=self.save_title_pic, meta={"rh_ylw_id": rh_ylw_id_for_pic})
                    else:
                        logger.error("parse error: [title_picture] : url: %s" % response.url)

            # get normal picture's src and send request
            normal_pictures = response.xpath('//div[@class="inst-photos"]/div[@class="cont"]/ul/li/a/img/@src').extract()
            for normal_picture in normal_pictures:
                if len(normal_picture) != 0:
                    yield scrapy.Request(url=normal_picture, callback=self.save_normal_pic, meta={"rh_ylw_id": rh_ylw_id_for_pic})

            yield self.parse_one_rh_item(response)
        except Exception as e:
            logger.critical("Error: parse_one_rh(), for url: %s" % response.url)
            logger.critical(e)

    def parse_one_rh_item(self, response):
        try:
            rhit = RestHomeItem()
            logger.debug("----------parse rh_name----------")
            rh_name = response.xpath('//div[@class="inst-summary"]/h1/text()').extract()
            logger.debug("rh_name: %s" % rh_name[0].strip());
            rhit['rh_name'] = rh_name[0].strip()
            logger.debug("----------parse rh_phone----------")
            rh_phone = response.xpath('//div[@class="inst-summary"]/ul/li/span/text()').extract()
            if len(rh_phone) != 0:
                rhit['rh_phone'] = rh_phone[0].strip()
            rh_phone = response.xpath('//div[@class="inst-summary"]/ul/li/a/@href').extract()
            if len(rh_phone) != 0:
                # special to indicate that phone number need to login, for exam: #41090
                logger.debug("[Warning] rh_phone: need login");
                rhit['rh_phone'] = "login"

            logger.debug("----------parse rh_ylw_id----------")
            rhit['rh_ylw_id'] = self.get_rh_ylw_id(response)
            logger.debug("rh_ylw_id: %s" % rhit['rh_ylw_id'])

            logger.debug("----------parse base info----------")
            page_item_values = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/text()').extract()
            page_item_keys = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/em/text()').extract()
            for page_item_idx, page_item_key in enumerate(page_item_keys):
                title = (
                    ('rh_location_id',   u'\u6240\u5728\u5730\u533a\uff1a'),     #1, '所在地区：'
                    ('rh_type',   u'\u673a\u6784\u7c7b\u578b\uff1a'),     #2, '机构类型：'
                    ('rh_factory_property',   u'\u673a\u6784\u6027\u8d28\uff1a'),     #3, '机构性质：'
                    ('rh_person_in_charge',   u'\u8d1f  \u8d23  \u4eba\uff1a'),       #4, '负 责 人：'
                    ('rh_establishment_time',   u'\u6210\u7acb\u65f6\u95f4\uff1a'),     #5, '成立时间：'
                    ('rh_floor_surface',   u'\u5360\u5730\u9762\u79ef\uff1a'),     #6, '占地面积：'
                    ('rh_building_area',   u'\u5efa\u7b51\u9762\u79ef\uff1a'),     #7, '建筑面积：'
                    ('rh_bednum',   u'\u5e8a\u4f4d\u6570\uff1a'),           #8, '床位数：'
                    ('rh_for_persons',   u'\u6536\u4f4f\u5bf9\u8c61\uff1a'),     #9, '收住对象：'
                    ('rh_charges_extent',   u'\u6536\u8d39\u533a\u95f4\uff1a'),     #10,'收费区间：'
                    ('rh_special_services',   u'\u7279\u8272\u670d\u52a1\uff1a'),     #11,'特色服务：'
                )
                for val in title:
                    if page_item_key == val[1]:
                        rhit[val[0].strip()] = page_item_values[page_item_idx].strip()
                        break;

            logger.debug("----------parse contact-info----------")
            # contact us
            idx = -1
            rh_contact_info = response.xpath('//div[@class="contact-info"]/div[@class="cont"]/ul/li/text()').extract()
            for quote in rh_contact_info:
                idx = idx + 1
                if idx > 1:
                    break
                title_1 = [
                    'rh_contact_person',  #1
                    'rh_address',  #2
                ]
                rhit[title_1[idx].strip()] = quote.strip()
            # 'rh_url',  #3
            logger.debug("----------parse contact-info---------- rh_transportation")
            rh_url = response.xpath('//div[@class="contact-info"]/div[@class="cont"]/ul/li/a/@href').extract()
            if len(rh_url) != 0 and len(rh_url[0]) != 0:
                # for exam: 228436.html
                rhit['rh_url'] = rh_url[0].strip()
            else:
                # for example: 27168.html
                if len(rh_contact_info) > 2 and len(rh_contact_info[2]) != 0:
                    rhit['rh_url'] = rh_contact_info[2].strip()

            # 'rh_transportation',  #4
            logger.debug("----------parse contact-info---------- rh_transportation")
            cond = '//div[@class="contact-info"]/div[@class="cont"]/ul/li[@class="traffic"]'
            transportation_0 = ""
            transportation = response.xpath(cond).extract()
            for i in transportation:
                transportation_0 = transportation_0 + i.strip()
            rhit['rh_transportation'] = transportation_0.strip()

            parse_whole_div_list = (\
                    ('rh_inst_intro', 'inst-intro'),\
                    ('rh_inst_charge', 'inst-charge'),\
                    ('rh_facilities', 'facilities'),\
                    ('rh_service_content', 'service-content'),\
                    ('rh_inst_notes', 'inst-notes'))
            for i in parse_whole_div_list:
                QuotesSpider.parseWholeDiv(response, rhit, i[0], i[1])

            return rhit
        except Exception as e:
            logger.critical("Error: parse_one_rh_item(), for url: %s" % response.url)
            logger.critical(e)

    @staticmethod
    def parseWholeDiv(response, item, key, key_content_class):
        try:
            info_0 = ""
            str_xpath = '//div[@class=\"' + key_content_class + '\"]/div[@class=\"cont\"]'
            info = response.xpath(str_xpath).extract()
            for i in info:
                info_0 = info_0 + i.strip()
            item[key] = info_0.strip()

            # for 228436, rh_facilities has iframe, which lead to content is too big for mysql
            str_xpath = '//div[@class=\"' + key_content_class + '\"]/div[@class=\"cont\"]/iframe/text()'
            info = response.xpath(str_xpath).extract()
            if len(info) != 0:
                item[key] = "iframe"
        except Exception as e:
            logger.critical("Error: parseWholeDiv() for url: %s" % response.url)
            logger.critical(e)

    def save_title_pic(self, response):
        try:
            logger.debug("parsing title picture to saving picture ... %s" % response.url)
            self.save_pic(response, True)
        except Exception as e:
            logger.critical("Error: save_title_pic, for url: %s" % response.url)
            logger.critical(e)

    def save_normal_pic(self, response):
        try:
            logger.debug("parsing normal picture to saving picture ... %s" % response.url)
            self.save_pic(response, False)
        except Exception as e:
            logger.critical("Error: save_normal_pic, for url: %s" % response.url)
            logger.critical(e)

    def save_pic(self, response, is_title):
        try:
            if not response.url.endswith("jpg") and not response.url.endswith("png"):
                return
            logger.debug("saving picture ... ... %s" % response.url)

            file_name = response.url[(response.url.rfind("/") + 1) :];
            picture_dir = os.path.join(self.__pic_root_path, response.meta["rh_ylw_id"])

            file_util.save_pic(picture_dir, file_name, is_title, response.body)
        except Exception as e:
            logger.critical("Error: save_pic, for url: %s" % response.url)
            logger.critical(e)


    def get_rh_ylw_id(self, response):
        last_html_file = response.url[response.url.rfind("/")+1 : len(response.url)]
        return RestHomeItem.getFirstNum(last_html_file)
