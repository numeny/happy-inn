import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://www.yanglao.com.cn/resthome/27168.html#m1',
            'http://www.yanglao.com.cn/resthome/27168.html#m2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
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
        '''
        idx = -1
        for quote in response.xpath('//div[@class="base-info"]/div[@class="cont"]/ul/li/text()').extract():
            idx = idx + 1
            title_0 = [
                'city',                 #1
                'type',                 #2
                'factory_property',     #3
                'person_in_charge',     #4
                'establishment_time',   #5
                'floor_surface',        #6
                'building_area',        #7
                'bednum',               #8
                'for_persons',          #9
                'charges_extent',       #10
                'special_services',     #11
            ]
            print('%s: %s' % (title_0[idx], quote))
            yield {
                title_0[idx]: quote
            }

        # contact us
        idx = -1
        for quote in response.xpath('//div[@class="contact-info"]/div[@class="cont"]/ul/li/text()').extract():
            idx = idx + 1
            title_1 = [
                'contact_person',       #1
                'address',              #2
                'url',                  #3
                'transportation',       #4
            ]
            print('%s: %s' % (title_1[idx], quote))
            yield {
                title_1[idx]: quote
            }
        # introduce
        quotes = ""
        for quote in response.xpath('//div[@class="cont"]/p/span/text()').extract():
            quotes = quotes + quote

        yield {
            "introduction": quotes
        }
        print('introduction: %s' % quotes)

        '''
        print('quote: %s' % quotes)
        yield {
            "introduction": quotes
        }
        '''
