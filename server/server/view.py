# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render
 
def start(request):
    context = {}
    if "pre_page" in request.POST:
        context['message'] = 'pre_page'#get_pre_page()
    if "next_page" in request.POST:
        context['message'] = 'next_page'#get_next_page()
    if "q" in request.POST:
        print('q in request.POST')
        context['message'] = "you input: " + request.POST['q']

    return render(request, 'index.html', context)

def search(request):
    return start(request)

'''
def start(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
