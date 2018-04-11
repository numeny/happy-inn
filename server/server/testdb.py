# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
 
from RHModel.models import rh
 
# 数据库操作
def testdb(request):
    test1 = rh(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")
