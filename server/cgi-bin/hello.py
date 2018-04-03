#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

# CGI处理模块
import cgi, cgitb 
import MySQLdb as mdb

sys.path.append("../../")  

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


print(rh_ylw_id)

print '</div>'
print '</body>'
print '</html>'
