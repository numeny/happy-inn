#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from tutorial.rest_home_item import RestHomeItem

total_idx = 0
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
#            'http://www.yanglao.com.cn/resthome/27168.html',
#            'http://www.yanglao.com.cn/resthome/41090.html',
#            'http://www.yanglao.com.cn/resthome/228436.html',
#            'http://www.yanglao.com.cn/resthome/40844.html',
            'http://www.yanglao.com.cn/xinjiang',
#            'http://www.yanglao.com.cn/resthome/22608.html',
#            'http://www.yanglao.com.cn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_idx
        # all province
        # get all url of privice's resthome list
        '''
        privince_url_list = response.xpath('//div[@class="hot-cities"]/dl/dd/a/@href').extract()
        for privince_url in privince_url_list:
            privince_url = "http://www.yanglao.com.cn" + privince_url
            print("privince_url: %s" % privince_url)
            yield scrapy.Request(url=privince_url, callback=self.parse)
        '''

        # all pages for one province
        '''
        total_idx = total_idx + 1
        # get next page of rest home list
        url_list_in_privince_text = response.xpath('//div[@class="pager"]/ul[@class="pages"]/li/a/text()').extract()
        url_list_in_privince_href = response.xpath('//div[@class="pager"]/ul[@class="pages"]/li/a/@href').extract()
        for idx in xrange(0, len(url_list_in_privince_text)):
            if url_list_in_privince_text[idx] == u'\u4e0b\u4e00\u9875':
                next_url_list_in_prinvice = "http://www.yanglao.com.cn" + url_list_in_privince_href[idx].strip()
                print("====total_idx: %d===== next_url_list_in_prinvice: %s" % (total_idx, next_url_list_in_prinvice))
                yield scrapy.Request(url=next_url_list_in_prinvice, callback=self.parse)
        '''

        # all url for one province's one page
        '''
        '''
        url_list_in_privince_one_page = response.xpath('//div[@class="restlist"]/div[@class="list-view"]/ul/li/div[@class="info"]/h4/a/@href').extract()
        print("====total_idx: %d===== url_list_in_privince_one_page: %s" % (total_idx, url_list_in_privince_one_page))
        for url in url_list_in_privince_one_page:
            url = "http://www.yanglao.com.cn" + url.strip()
            print("----------parse start: %d, url: %s" % (total_idx, url))
            yield scrapy.Request(url=url, callback=self.parse_item_from_response)

        yield self.parse_item_from_response(response)

    def parse_item_from_response(self, response):
        print("Parse item start ... %s" % response.url)
        rhit = RestHomeItem()

        print("----------parse rh_name----------")
        rh_name = response.xpath('//div[@class="inst-summary"]/h1/text()').extract()
        print("rh_name: %s" % rh_name[0].strip());
        rhit['rh_name'] = rh_name[0].strip()
        '''
        yield {
            "rh_name" : rh_name[0].strip()
        }
        '''
        print("----------parse rh_phone----------")
        rh_phone = response.xpath('//div[@class="inst-summary"]/ul/li/span/text()').extract()
        if len(rh_phone) != 0:
            print("rh_phone: %s" % rh_phone[0].strip());
            rhit['rh_phone'] = rh_phone[0].strip()
            '''
            yield {
                "rh_phone" : rh_phone[0].strip()
            }
            '''
        rh_phone = response.xpath('//div[@class="inst-summary"]/ul/li/a/@href').extract()
        if len(rh_phone) != 0:
            # special to indicate that phone number need to login, for exam: #41090
            print("[Warning] rh_phone: need login");
            rhit['rh_phone'] = "login"

        print("----------parse rh_ylw_id----------")
        last_html_file = response.url[response.url.rfind("/")+1 : len(response.url)]
        rhit['rh_ylw_id'] = RestHomeItem.getFirstNum(last_html_file)
        print("rh_ylw_id: %s" % rhit['rh_ylw_id'])

        print("----------parse base info----------")
        page_item_values = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/text()').extract()
        page_item_keys = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/em/text()').extract()
        for page_item_idx in xrange(0, len(page_item_keys)):
            page_item_key = page_item_keys[page_item_idx]
            title_0 = {
                'rh_location_id':   u'\u6240\u5728\u5730\u533a\uff1a',     #1, '所在地区：'
                'rh_type':   u'\u673a\u6784\u7c7b\u578b\uff1a',     #2, '机构类型：'
                'rh_factory_property':   u'\u673a\u6784\u6027\u8d28\uff1a',     #3, '机构性质：'
                'rh_person_in_charge':   u'\u8d1f  \u8d23  \u4eba\uff1a',       #4, '负 责 人：'
                'rh_establishment_time':   u'\u6210\u7acb\u65f6\u95f4\uff1a',     #5, '成立时间：'
                'rh_floor_surface':   u'\u5360\u5730\u9762\u79ef\uff1a',     #6, '占地面积：'
                'rh_building_area':   u'\u5efa\u7b51\u9762\u79ef\uff1a',     #7, '建筑面积：'
                'rh_bednum':   u'\u5e8a\u4f4d\u6570\uff1a',           #8, '床位数：'
                'rh_for_persons':   u'\u6536\u4f4f\u5bf9\u8c61\uff1a',     #9, '收住对象：'
                'rh_charges_extent':   u'\u6536\u8d39\u533a\u95f4\uff1a',     #10,'收费区间：'
                'rh_special_services':   u'\u7279\u8272\u670d\u52a1\uff1a',     #11,'特色服务：'
            }
            # print('page_item_key: \"%x\"' % (page_item_key[0]));
            for idx in xrange(0, len(title_0.values())):
                if page_item_key == title_0.values()[idx]:
                    print('%s : %s, \"%s\"' % (idx, title_0.keys()[idx], page_item_values[page_item_idx].strip()));
                    rhit[title_0.keys()[idx].strip()] = page_item_values[page_item_idx].strip()
                    '''
                    yield {
                        title_0.keys()[idx].strip(): page_item_values[page_item_idx].strip()
                    }
                    '''
                    break;

        print("----------parse contact-info----------")
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
            '''
            yield {
                title_1[idx]: quote
            }
            '''
        # 'rh_url',  #3
        print("----------parse contact-info---------- rh_transportation")
        rh_url = response.xpath('//div[@class="contact-info"]/div[@class="cont"]/ul/li/a/@href').extract()
        if len(rh_url) != 0 and len(rh_url[0]) != 0:
            # for exam: 228436.html
            rhit['rh_url'] = rh_url[0].strip()
        else:
            # for example: 27168.html
            if len(rh_contact_info) > 2 and len(rh_contact_info[2]) != 0:
                rhit['rh_url'] = rh_contact_info[2].strip()

        # 'rh_transportation',  #4
        print("----------parse contact-info---------- rh_transportation")
        cond1 = '//div[@class="contact-info"]/div[@class="cont"]/ul/li[@class="traffic"]/text()'
        cond2 = '//div[@class="contact-info"]/div[@class="cont"]/ul/li[@class="traffic"]/p/text()' #40636
        cond3 = '//div[@class="contact-info"]/div[@class="cont"]/ul/li[@class="traffic"]/p/strong/span/text()' #40844
        cond = cond1 + ' | ' + cond2 + ' | ' + cond3
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

        # facilities 设施
        '''
        print("----------parse facilities----------")
        facilities = response.xpath('//div[@class="facilities"]/div[@class="cont"]/text()').extract()
        if len(facilities) != 0:
            fac = facilities[0].strip()
            if len(fac) == 0:
                facilities = response.xpath('//div[@class="facilities"]/div[@class="cont"]/span/text()').extract()
                if len(facilities) != 0:
                    fac = fac + facilities[0].strip()
                facilities = response.xpath('//div[@class="facilities"]/div[@class="cont"]/span/span/text()').extract()
                for f in facilities:
                    fac = fac + f.strip()
            print('rh_facilities: %s' % fac)
            rhit['rh_facilities'] = fac.strip()
        '''

        return rhit

    @staticmethod
    def parseWholeDiv(response, item, key, key_content_class):
        print("----------parse %s----------" % key)

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
