# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.rest_home_item import RestHomeItem

from db.sql import RhSql

class TutorialPipeline(object):
    def process_item(self, item, spider):
        print("")
        print("")
        print("****** TutorialPipeline::process_item ********************************-0")
        for i in item.keys():
            print("%s: %s" % (i, item[i]))
        sql = RhSql()
        RestHomeItem.init_item_field_to_default_if_null(item)
        sql.insert_data(item)
        return item
