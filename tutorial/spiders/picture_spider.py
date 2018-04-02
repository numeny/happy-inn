#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import scrapy

class PictureSpider(scrapy.Spider):
    name = "picture"

    __pic_root_path = "result/picture"

    def start_requests(self):
        try:
            if os.path.exists(self.__pic_root_path):
                PictureSpider.rmdir_recursive(self.__pic_root_path)
            os.makedirs(self.__pic_root_path)
        except Exception as e:
            print(e)

        urls = [
            'http://www.yanglao.com.cn/resthome/27168.html',
            'http://www.yanglao.com.cn/resthome/41090.html',
            'http://www.yanglao.com.cn/resthome/228436.html',
#            'http://www.yanglao.com.cn/xinjiang',
#            'http://www.yanglao.com.cn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("parsing picture's url ...")
        if response.url.endswith("html"):
            # get title picture's src and send request
            title_picture = response.xpath('//div[@class="inst-info"]/div[@class="cont"]/div[@class="inst-pic"]/img/@src').extract()
            if len(title_picture) != 0:
                yield scrapy.Request(url=title_picture[0], callback=self.parse)

            # get normal picture's src and send request
            inst_photos = response.xpath('//div[@class="inst-photos"]/div[@class="cont"]/ul/li/a/img/@src').extract()
            for i in inst_photos:
                if len(i) != 0:
                    print("inst_photos url: %s" % i)
                    yield scrapy.Request(url = i, callback=self.parse)

        if not response.url.endswith("jpg") and not response.url.endswith("png"):
            return

        print("parsing picture to saving picture ...")
        url_len = len(response.url)
        url_last = response.url.rfind("/")
        url_last_two = response.url.rfind("/", 0, url_last)
        print(url_last)
        print(url_last_two)
        file_name = response.url[(url_last + 1) : url_len];
        ylw_resthome_id = response.url[(url_last_two + 1) : url_last]
        print(file_name)
        print(ylw_resthome_id)

        resthome_id = ylw_resthome_id
        picture_dir = os.path.join(self.__pic_root_path, resthome_id)
        filename = os.path.join(picture_dir, file_name)

        try:
            if not os.path.exists(picture_dir):
                os.makedirs(picture_dir)
        except Exception as e:
            print(e)

        with open(filename, 'wb') as f:
            f.write(response.body)

    @staticmethod
    def rmdir_recursive(top):
        try:
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except Exception as e:
            print(e)
