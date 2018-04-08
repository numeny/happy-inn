#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from tutorial.rest_home_item import RestHomeItem

total_idx = 0
class YLInfoRestHomeSpider(scrapy.Spider):
    name = "YLInfoRestHome"
    __host_pc = "http://www.yanglaocn.com"
    __host_mobile = "http://m.yanglaocn.com"

    def start_requests(self):
        '''
        url = 'http://m.yanglaocn.com/useradmin/usermsg.php?ajaxtype=popupmsgshow&rand=0.26601639980108116'
        yield scrapy.Request(url=url, callback=self.parse, headers={\
            "X-Requested-With": "XMLHttpRequest",\
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36",\
            "Referer": "http://www.yanglaocn.com/shtml/ylyxx/2014-11/yly141612656322899.html",\
            "Cookie": "ipcity=%E5%8C%97%E4%BA%AC%E5%B8%82; yunsuo_session_verify=495ef87c27376ca65608c571a859a5a4; PHPSESSID=b108eb064070ba105f48cf8d384e5c25; Hm_lvt_6168556b0a921e8d0375330e702bc0fe=1522909169,1522981374,1522993601,1522996985; Hm_lpvt_6168556b0a921e8d0375330e702bc0fe=1522999936",\
        })
#for url in urls:
        url = 'http://m.yanglaocn.com/yanglaoyuan/yanglaoyuanxx.php?ajaxtype=yanglaoxx_showlianxi&rand=0.0688758497167421'
#for url in urls:
#yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url=url, callback=self.parse, method='post', headers={\
            "X-Requested-With":"XMLHttpRequest",\
            "Origin": "http://www.yanglaocn.com",\
            "Referer": "http://www.yanglaocn.com/shtml/ylyxx/2012-04/yly1335281469113.html",\
            "Accept-Encoding": "gzip, deflate"\
        })
        '''
        urls = [
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=0',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=022',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=0955',
            'http://m.yanglaocn.com/shtml/ylyxx/2016-04/yly146172868824614.html'
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=02201&page=2',
#            'http://www.yanglaocn.com/yanglaoyuan/yly',
#            'http://www.yanglaocn.com/yanglaoyuan/yly/?RgSelect=01001&gotoip=y',
#            'http://m.yanglaocn.com/shtml/ylyxx/2014-06/yly140411449322841.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_idx
        print(" starting parse privince list ... response: %s" % response.url)
        print(" starting parse privince list ... response: %s" % response.body)
        '''
        title_str = "RgSelect="
        area_url_start_idx = response.url.find(title_str) + len(title_str)
        area_url = response.url[area_url_start_idx: len(response.url)]
        print(" starting parse privince list ... area_url: %s" % area_url)
        if len(area_url) <= 1: #avoid parsing the area's page of one privince
            # all province
            # get all url of privice's resthome list
            privince_url_list = response.xpath('//div[@class="querywhere"]/div[@class="sanxiantj"]/div[@class="jigouquyu_right"]/label/a/@href').extract()
# print(privince_url_list)
            for privince_url in privince_url_list:
                print("privince_url: %s" % privince_url)
                yield scrapy.Request(url=privince_url, callback=self.parse)
        '''
        '''
        # get next page of rest home list
        print(" starting parse rest home list for one page of one privince ...")
        anchor_list_next_page_in_privince = response.xpath('//div[@class="main"]/div[@class="page"]/div[@class="webpage"]/a').extract()
        print(anchor_list_next_page_in_privince)
        for x in anchor_list_next_page_in_privince:
            m = Selector(text=x).xpath("//a/span/text()").extract()
            str_next_page = u'\u4e0b\u4e00\u9875' # next_page
            if len(m) > 0 and not cmp(str_next_page, m[0]):
                print("777777777777777")
                n = Selector(text=x).xpath("//a/@href").extract()
                print("n: ")
                print(n)
                print("")
                print("")
                if len(n) > 0:
                    print("1")
                    url_next_page = response.url[:response.url.rfind('/')] + n[0]
                    print("2: %s" % url_next_page)
                    yield scrapy.Request(url=url_next_page, callback=self.parse)

            print(m)
        '''

        print("88888888888888888888")
        # all url for one province's one page
        url_list_in_privince_one_page = response.xpath('//div[@class="querywhere2"]/div[@class="jiadiantucontext"]/div[@class="jiadiantucontext_ul"]/a/@href').extract()
        print(url_list_in_privince_one_page)
        for u in url_list_in_privince_one_page:
            u = u.replace("www", "m")
            print(u)
            yield scrapy.Request(url=u, callback=self.parse)
        print("99999999999999999999999999")
        '''
        url_list_in_privince_one_page = response.xpath('//div[@class="restlist"]/div[@class="list-view"]/ul/li/div[@class="info"]/h4/a/@href').extract()
        print("====total_idx: %d===== url_list_in_privince_one_page: %s" % (total_idx, url_list_in_privince_one_page))
        for url in url_list_in_privince_one_page:
            url = "http://www.yanglao.com.cn" + url.strip()
            print("----------parse start: %d, url: %s" % (total_idx, url))
            yield scrapy.Request(url=url, callback=self.parse_item_from_response)
        '''

        yield self.parse_item_from_response(response)

    def parse_item_from_response(self, response):
        print("Parse item start ... %s" % response.url)
        '''
        '''
        rhit = RestHomeItem()

        print("")
        print("parsing basicInformation ...")
        print("")
        # basicInformation
        self.fill_item_with_list(rhit, response)
        rh_name = response.xpath('//div[@id="BasicInformation"]/div[@class="leftcontexttitle"]/label/text()').extract()
        if len(rh_name) > 0:
            rhit['rh_name'] = rh_name[0]

        # Contact US info
        print("")
        print("parsing ContactUsList ...")
        print("")
        self.fill_item_with_list(rhit, response)
        rh_url = response.xpath('//div[@id="ContactUsList"]/div[@class="leftcontexttitle"]/a/@href').extract()
        if len(rh_url) > 0:
            rhit['rh_url'] = rh_url[0]
        if 'rh_contact_person' in rhit:
            rhit['rh_person_in_charge'] = rhit['rh_contact_person']

        # OrganizationsOn_Text
        print("")
        print("parsing OrganizationsOn etc ...")
        print("")
        self.fill_item_with_p_lable_list(rhit, response)

        # for exam: m.yanglaocn.com/shtml/ylyxx/2013-04/yly1365591790411.html
        rhit['rh_ylw_id'] = "ff-" + response.url[response.url.find("ylyxx") + len("ylyxx") + 1:]
        rhit['rh_ylw_id'] = rhit['rh_ylw_id'].replace(".html", "")
        RestHomeItem.printSelf(rhit)
        return rhit

    def fill_item_with_list(self, rhit, response):
        print("start fill_item_with_list-0 ...")
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

        print("start fill_item_with_list-1 ...")
        for i in item_list:
            print("start parsing lefttitle -1: %s" % i[0])
            str_xpath = '//div[@id="' + i[0] + '"]/div[@class="leftcontexttitle"]/text()'
            leftcontexttitle_list = response.xpath(str_xpath).extract()
            print(leftcontexttitle_list)
            for idx, val in enumerate(i[1]):
                print("start parsing lefttitle -2: %s" % val)
                if len(leftcontexttitle_list) > idx and len(leftcontexttitle_list[idx].strip()) > 0:
                    rhit[val] = leftcontexttitle_list[idx].strip()
                    print("start parsing lefttitle -3: %s" % rhit[val])


    def fill_item_with_p_lable_list(self, rhit, response):
        print("start fill_item_with_p_lable_list-1 ...")
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
            print("start str_xpath -1 ... %s" % i[0])
            info = response.xpath(str_xpath).extract()
            print(info)
            str_info = ""
            for j in info:
                str_info = str_info + j
            if len(str_info) > 0:
                rhit[i[1]] = str_info
