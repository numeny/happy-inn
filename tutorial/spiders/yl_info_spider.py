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
        print(" starting parse privince list ... response: %s" % response.url)
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

        self.parse_item_from_response(response)

    def parse_item_from_response(self, response):
        print("Parse item start ... %s" % response.url)
        '''
        '''
        rhit = RestHomeItem()

        results_mymain_xpath = response.xpath('//div[@class="mymain"]').extract()
        print("results_mymain_xpath:")
        print("")
        rh_inst_intro = ""
        for result_mymain_xpath in results_mymain_xpath:
            print("result_mymain_xpath-1:")
            print(result_mymain_xpath)
            lefttitle = Selector(text=result_mymain_xpath).xpath('//div[@class="mymain"]/div[@class="lefttitle"]/span/text()').extract()
            leftcontexttitle = Selector(text=result_mymain_xpath).xpath('//div[@class="mymain"]/div[@class="leftcontexttitle"]/text()').extract()
            print("")
            print("lefttitle:")
            print(lefttitle)
            print("leftcontexttitle:")
            print(leftcontexttitle)
            print("")
            print("")
            if len(lefttitle) <= 0:
                continue
            self.fill_item_with_list(lefttitle, leftcontexttitle, result_mymain_xpath)

        print("----------parse start pring item----------rh_phone-4")
        RestHomeItem.printSelf(rhit)

        '''
            if !cmp(lefttitle[0], "Organizations On"):
                organizations_on_info = Selector(text=result_mymain_xpath).xpath('//div[@class="leftcontext"]/div[@class="leftcontextmessage"]/p').extract()
                print(organizations_on_info)
                for i in organizations_on_info:
                    rhit['rh_inst_intro'] = rhit['rh_inst_intro'] + i.strip()

            if !cmp(lefttitle[0], "Check-in Notes"):
                check_in_notes = Selector(text=result_mymain_xpath).xpath('//div[@class="leftcontext"]/div[@class="leftcontextmessage"]/p').extract()
                print(organizations_on_info)
                for i in organizations_on_info:
                    rhit['rh_inst_intro'] = rhit['rh_inst_intro'] + i.strip()
        '''

    def fill_item_with_list(self, lefttitle, leftcontexttitle, one_result_mymain_xpath):
        print("start fill_item_with_list-0 ...")
        lefttitle_list = (
            'Basic Information',
            'Contact Us',
            'Organizations On',
            'Environmental Facilities',
            'Service Object',
            'Check-in Notes',
            'Fee Scale',
            'Traffic Information'
        )
        key_lists = (
                 ('rh_establishment_time',
                 'rh_bednum',
                 'rh_floor_surface',
                 'rh_for_persons',
                 'rh_charges_extent',
                 'rh_type',
                 'rh_factory_property'),
                ('rh_person_in_charge',
                 'rh_contact_person',
                 'rh_phone',
                 'rh_mobile',
                 'rh_email',
                 'rh_postcode',
                 'rh_location_id',
                 'rh_address'),
                ('rh_inst_intro'),
                ('rh_facilities'),
                ('rh_service_content'),
                ('rh_inst_notes'),
                ('rh_inst_charge'),
                ('rh_transportation')
                )

        print("start fill_item_with_list-1 ...")
        for idx, l in enumerate(lefttitle_list):
            print("start fill_item_with_list-2 ...")
            print("start parsing lefttitle -0: %s" % lefttitle[0])
            if cmp(l, lefttitle[0]):
                continue
            print("start parsing lefttitle -0: %s" % l)
            # Basic Information
            for idx1, val in enumerate(key_lists[idx]):
                print("start parsing item : %s" % val)
                idx2 = idx1
                if not cmp("Basic Information", lefttitle[0]):
                    idx2 = idx2 + 1
                print("start parsing item : %d, %s" % (idx2, leftcontexttitle[idx2].strip()))
                print("start parsing item : %d, %d" % (idx2, len(leftcontexttitle)))
                if len(leftcontexttitle) > idx2:
                    print("start parsing item : %d, %d" % (idx2, len(leftcontexttitle)))
                    print("start parsing item : val: %s" % (val))
                    rhit[val] = leftcontexttitle[idx2].strip()
                    print("start parsing item : val: %s" % (val))
                    print("start parsing item : set item: %s, %s" % (val, leftcontexttitle[idx2].strip()))
            if not cmp("Basic Information", lefttitle[0]):
                print("start parsing rh_name_info")
                rh_name_info = Selector(text=one_result_mymain_xpath).xpath('//div[@class="mymain"]/div[@class="leftcontexttitle"]/lable/text()').extract()
                print("rh_name_info:")
                print(rh_name_info)
                if len(rh_name_info) > 0:
                    rhit['rh_name'] = rh_name_info[0].strip()

            if not cmp("Contact Us", lefttitle[0]):
                url_info = Selector(text=one_result_mymain_xpath).xpath('//div[@class="mymain"]/div[@class="leftcontexttitle"]/a/@href').extract()
                if len(url_info) > 0:
                    rhit["rh_url"] = url_info[0].strip()

#rhit['rh_ylw_id'] = ret_xpath[0].strip()
#yield rhit
