#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

# CGI处理模块
import cgi, cgitb 
import MySQLdb as mdb

sys.path.append("../../")  

from sql import RhSql

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage() 

# 获取数据
rh_ylw_id = form.getvalue('id')

print "Content-type:text/html"
print
print '<html>'
print '<head>'
print '<title>Hello</title>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
print '<title>Example website</title>'
print '</head>'
print '<body>'
print '<h2>Hello Word! This is my first CGI program</h2>'
print '<div>'

print("rh_ylw_id: %s" % rh_ylw_id)
sql = RhSql()
rec = sql.select_one_rh_ylw_id(rh_ylw_id)
for i in rec:
    for j in i:
        print('<p>')
        print(j)
        print('</p>')

print '</div>'
print '</body>'
print '</html>'
