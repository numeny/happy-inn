# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render
 
def start(request):
    context = {}
    if "q" in request.POST:
        context['message'] = "you input: " + request.POST['q']
    return render(request, 'index.html', context)

def search(request):
    return start(request)

'''
def start(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
