#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
'''
2018-04-10 20:41:06 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET http://www.yanglao.com.cn/resthome/8086.html> (failed 1 times): 500 Internal Server Error
'''

a = open("/tmp/log.1")
db = open("/tmp/log.2")

a0 = a.readline()
while a0:
    found = False
    db0 = db.readline()
    while db0:
        if not cmp(a0, db0):
            found = True
        db0 = db.readline()
    if not found:
        print(a0)
    a0 = a.readline()
    db.seek(os.SEEK_SET);
