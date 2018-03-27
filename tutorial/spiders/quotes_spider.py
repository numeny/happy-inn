# -*- coding: UTF-8 -*-
import scrapy

total_idx = 0
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
#            'http://www.yanglao.com.cn/resthome/27168.html',

#            'http://www.yanglao.com.cn/resthome/41090.html',
            'http://www.yanglao.com.cn/xinjiang',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global total_idx
        '''
        # get all url of privice's resthome list
        privince_url_list = response.xpath('//div[@class="hot-cities"]/dl/dd/a/@href').extract()
        for privince_url in privince_url_list:
            privince_url = "http://www.yanglao.com.cn" + privince_url
            print("privince_url: %s" % privince_url)
            yield scrapy.Request(url=privince_url, callback=self.parse)
        '''

        total_idx = total_idx + 1
        url_list_in_privince_text = response.xpath('//div[@class="pager"]/ul[@class="pages"]/li/a/text()').extract()
        url_list_in_privince_href = response.xpath('//div[@class="pager"]/ul[@class="pages"]/li/a/@href').extract()
        for idx in xrange(0, len(url_list_in_privince_text)):
            if url_list_in_privince_text[idx] == u'\u4e0b\u4e00\u9875':
                next_url_list_in_prinvice = "http://www.yanglao.com.cn" + url_list_in_privince_href[idx].strip()
                print("====total_idx: %d===== next_url_list_in_prinvice: %s" % (total_idx, next_url_list_in_prinvice))
                yield scrapy.Request(url=next_url_list_in_prinvice, callback=self.parse)

        url_list_in_privince_one_page = response.xpath('//div[@class="restlist"]/div[@class="list-view"]/ul/li/div[@class="info"]/h4/a/@href').extract()
        print("====total_idx: %d===== url_list_in_privince_one_page: %s" % (total_idx, url_list_in_privince_one_page))
        for url in url_list_in_privince_one_page:
            url = "http://www.yanglao.com.cn" + url.strip()
            print("----------parse start: %d, url: %s" % (total_idx, url))
            yield scrapy.Request(url=url, callback=self.parse)

        print("----------parse start: %d" % (total_idx))
        '''
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        print('Saved file %s' % filename)

        # print('savedData: ' $ response.css('div.cont ul li').extract())
        # for quote in response.css('div.cont ul li'):
        # base info
        '''
        rh_name = response.xpath('//div[@class="inst-summary"]/h1/text()').extract()
        print("rh_name: %s" % rh_name[0].strip());
        yield {
            "rh_name" : rh_name[0].strip()
        }
        rh_phone = response.xpath('//div[@class="inst-summary"]/ul/li/span/text()').extract()
        if len(rh_phone) != 0:
            print("rh_phone: %s" % rh_phone[0].strip());
            yield {
                "rh_phone" : rh_phone[0].strip()
            }
        page_item_values = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/text()').extract()
        page_item_keys = response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/em/text()').extract()
        for page_item_idx in xrange(0, len(page_item_keys)):
            page_item_key = page_item_keys[page_item_idx]
            title_0 = {
                'rh_city':   u'\u6240\u5728\u5730\u533a\uff1a',     #1, '所在地区：'
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
                    yield {
                        title_0.keys()[idx].strip(): page_item_values[page_item_idx].strip()
                    }
                    break;

        # contact us
        idx = -1
        for quote in response.xpath('//div[@class="contact-info"]/div[@class="cont"]/ul/li/text()').extract():
            idx = idx + 1
            title_1 = [
                'rh_contact_person',  #1
                'rh_address',  #2
                'rh_url',  #3
                'rh_transportation',  #4
            ]
            print('%s: %s' % (title_1[idx], quote))
            yield {
                title_1[idx]: quote
            }

        # introduction
        inst_intro = ""
        introductions = response.xpath('//div[@class="inst-intro"]/div[@class="cont"]/text()').extract()
        for i in introductions:
            inst_intro = inst_intro + i.strip()
        introductions_2 = response.xpath('//div[@class="inst-intro"]/div[@class="cont"]/span/text()').extract()
        for i in introductions_2:
            inst_intro = inst_intro + i.strip()
        introductions_3 = response.xpath('//div[@class="inst-intro"]/div[@class="cont"]/p/span/text()').extract()
        for i in introductions_3:
            inst_intro = inst_intro + i.strip()

        print('rh_inst_intro: %s' % inst_intro)
        yield {
            "rh_inst_intro": inst_intro
        }

        # facilities 设施
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
            yield {
                "rh_facilities": fac.strip()
            }

        # service-content 服务内容
        service_content = response.xpath('//div[@class="service-content"]/div[@class="cont"]/text()').extract()
        if len(service_content) != 0:
            service = service_content[0].strip()
            print('rh_service_content: %s' % service)
            yield {
                "rh_service_content": service
            }

        # inst-notes 入住须知 FIXME format \n\t
        inst_notes = response.xpath('//div[@class="inst-notes"]/div[@class="cont"]/p/text()').extract()
        if len(inst_notes) != 0:
            info =""
            for i in inst_notes: info = info + i.strip()
            if len(info) == 0:
                inst_notes = response.xpath('//div[@class="inst-notes"]/div[@class="cont"]/p/span/text()').extract()
                for i in inst_notes: info = info + i.strip()
            print('rh_inst_notes: %s' % info)
            yield {
                "rh_inst_notes": info
            }

        

        '''
        # get new join rest home
        new_join_list = response.xpath('//div[@class="rbox new-join"]/div[@class="cont"]/ul[@class="txtlist"]/li/a/@href').extract()
        for new_join in new_join_list:
            new_url = "http://www.yanglao.com.cn" + new_join
            yield scrapy.Request(url=new_url, callback=self.parse)
        '''
