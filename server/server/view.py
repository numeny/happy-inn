# -*- coding: utf-8 -*-
 
import sys

from django.http import HttpResponse
from django.shortcuts import render

sys.path.append("../../")
sys.path.append("./")
sys.path.append("../")

reload(sys)

from sql import RhSql
from RHModel.models import rh
 
curr_index = 0
def start(request):
    global curr_index
    context = {}
    if "pre_page" in request.POST:
        context['message'] = 'pre_page'#get_pre_page()
        curr_index = curr_index - 1
    if "next_page" in request.POST:
        context['message'] = 'next_page'#get_next_page()
        curr_index = curr_index + 1
    if "q" in request.POST:
        print('q in request.POST')
        context['message'] = "you input: " + request.POST['q']

    db = rh.objects.all()
    print(db[0])
    if curr_index <= 0:
        curr_index = 0
    context['record'] = db[curr_index]
    return render(request, 'index.html', context)

def search(request):
    return start(request)

'''
def start(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
