from django.shortcuts import render_to_response

from apps.ewatch.models import *

def index(request):
    return render_to_response('ewatch/base.html')

def scrape_details(request):
    tdata = {}
    # percent of past classes scraped
    scraped_c = UpdateCheckClass.objects.values_list('class_pk', flat=True)
    tdata['classes_scraped'] = len(set(scraped_c))
    tdata['total_classes'] = Class.objects.all().count()
    tdata['percent_classes_scraped'] = round((tdata['classes_scraped']/ \
            tdata['total_classes'])*100)
    # percent of class scrapes succuessful (ie. has course name)
    
    # percent of registrations scrapes sucuessful (ie. has name)
    
    return render_to_response('ewatch/scrape_details.html', tdata)

def list_classes(request):
    tdata = {'classes': []}
    
    return render_to_response('ewatch/list_classes.html', tdata)
