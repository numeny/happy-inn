# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.rest_home_item import RestHomeItem

from tutorial.sql import RhSql

class TutorialPipeline(object):
    def process_item(self, item, spider):
        print("")
        print("")
        print("TutorialPipeline::process_item********************************")
        '''
        '''
        for i in item.keys():
            print("%s: %s" % (i, item[i]))
        sql = RhSql()
        sql.insert_data(item)
        return item
