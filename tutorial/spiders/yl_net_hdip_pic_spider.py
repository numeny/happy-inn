#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time

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
    name = "hdpi-pic"
    __pic_root_path = os.path.join("result", "picture")

    headers = {
        "Referer":"http://onlinelibrary.wiley.com/journal/10.1002/(ISSN)1521-3773",
    }
    __retry_url_map = {}
    __MAX_RETRY_COUNT = 5

    def start_requests(self):
        logger.info("start_requests ...")
        file_util.create_dir(self.__pic_root_path)
        urls = [
#            'http://www.yanglao.com.cn/tianjin',
#            'http://www.yanglao.com.cn/resthome/8086.html',
#            'http://www.yanglao.com.cn/resthome/20671.html',
#            'http://www.yanglao.com.cn/resthome/20665.html',
            'http://www.yanglao.com.cn/resthome/20666.html',
#            'http://www.yanglao.com.cn/resthome/226645.html',
#            'http://www.yanglao.com.cn/resthomeImage/view/id/29452',
#            'http://www.yanglao.com.cn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
        '''
        with open("/tmp/list.not.insert") as a:
            a0 = a.readline()
            while a0:
                a0 = a0.replace("\n", "");
                if len(a0) != 0:
                    url = 'http://www.yanglao.com.cn/resthome/' + a0 + '.html'
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse)
                a0 = a.readline()
        '''

    def parse(self, response):
        global total_privinces
        global total_pages
        global total_idx
        try:

            print("parse ... url: %s" % response.url)
            # retry request if failed
            if response.status == 404:
                if __retry_url_map.has_key(response.url):
                    retry_cnt = __retry_url_map[response.url] + 1
                else:
                    retry_cnt = 1
                __retry_url_map[response.url] = retry_cnt
                if retry_cnt < __MAX_RETRY_COUNT:
                    logger.debug("Failed 404: retry send request times [%d] for url: %s" % (retry_cnt, response.url))
                    yield scrapy.Request(url=response.url, headers=self.headers, callback=self.parse)
                else:
                    logger.critical("Failed 404: request url: %s, exceed max retry time: %d" % response.url, __MAX_RETRY_COUNT)
                    logger.critical(e)

            '''
        # all province
        # get all url of privice's resthome list
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
            print("parse_one_rh ... url: %s" % response.url)
            # retry request if failed
            if response.status == 404:
                if __retry_url_map.has_key(response.url):
                    retry_cnt = __retry_url_map[response.url] + 1
                else:
                    retry_cnt = 1
                __retry_url_map[response.url] = retry_cnt
                if retry_cnt < __MAX_RETRY_COUNT:
                    logger.debug("Failed 404: retry send request times [%d] for url: %s" % (retry_cnt, response.url))
                    yield scrapy.Request(url=response.url, callback=self.parse)
                else:
                    logger.critical("Failed 404: request url: %s, exceed max retry time: %d" % response.url, __MAX_RETRY_COUNT)
                    logger.critical(e)
            '''
            print("parse_one_rh-1 ... url: %s" % response.url)
            # start picture
            # get web page url of all hdpi pictures
            web_page_url_list = response.xpath('//div[@class="inst-photos"]/div[@class="cont"]/ul/li/a/@href').extract()
            for web_page_url in web_page_url_list:
                logger.debug("requesting hdpi picture's web page ... %s" % web_page_url)
                rh_ylw_id_for_pic = self.get_rh_ylw_id(response)
                if len(web_page_url) > 0:
                    yield scrapy.Request(url=web_page_url, headers=self.headers, callback=self.parse, meta={"rh_ylw_id": rh_ylw_id_for_pic})

            hdip_pic = response.xpath('//div[@class="layout"]/div[@class="image-view"]/div[@id="imagebox"]/div[@id="bigpics"]/img/@src').extract()
            if len(hdip_pic) > 0 and len(hdip_pic[0]) > 0:
                logger.debug("requesting hdpi picture ... %s ... ylw_id: %s" % (hdip_pic[0], response.meta["rh_ylw_id"]))
                yield scrapy.Request(url=hdip_pic[0], headers=self.headers, callback=self.save_hdpi_pic, meta={"rh_ylw_id": response.meta["rh_ylw_id"]})
        except Exception as e:
            logger.critical("Error: parse_one_rh(), for url: %s" % response.url)
            logger.critical(e)

    def save_hdpi_pic(self, response):
        try:
            logger.debug("parsing hdpi picture to saving picture ... %s" % response.url)
            self.save_pic(response, False, True)
        except Exception as e:
            logger.critical("Error: save_hdpi_pic, for url: %s" % response.url)
            logger.critical(e)

    def save_pic(self, response, is_title):
        self.save_pic(response, is_title, False)

    def save_pic(self, response, is_title, is_hdpi):
        try:
            if not response.url.endswith("jpg") and not response.url.endswith("png"):
                return
            logger.debug("saving picture ... ... %s" % response.url)

            file_name = response.url[(response.url.rfind("/") + 1) :];
            picture_dir = os.path.join(self.__pic_root_path, response.meta["rh_ylw_id"])

            file_util.save_pic(picture_dir, file_name, is_title, is_hdpi, response.body)
        except Exception as e:
            logger.critical("Error: save_pic, for url: %s" % response.url)
            logger.critical(e)


    def get_rh_ylw_id(self, response):
        last_html_file = response.url[response.url.rfind("/")+1 : len(response.url)]
        return RestHomeItem.getFirstNum(last_html_file)
