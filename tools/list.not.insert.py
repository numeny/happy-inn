#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
'''
2018-04-10 20:41:06 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET http://www.yanglao.com.cn/resthome/8086.html> (failed 1 times): 500 Internal Server Error
'''

a = open("/tmp/list.not.insert")

with open("/tmp/list.not.insert") as a:
    a0 = a.readline()
    while a0:
        if len(a0) != 0:
            a0 = a0.replace("\n", "");
            print(a0)
        a0 = a.readline()
