from django.shortcuts import render_to_response

from apps.ewatch.models import Class, Registration, UpdateCheckClass

def index(request):
    return render_to_response('ewatch/base.html')

def scrape_details(request):
    tdata = {}
    scraped = UpdateCheckClass.objects.values_list('class_pk', flat=True)
    tdata['classes_scraped'] = len(set(scraped))
    tdata['total_classes'] = Class.objects.all().count()
    tdata['percent_classes_scraped'] = round((tdata['classes_scraped']/ \
            tdata['total_classes'])*100)
    return render_to_response('ewatch/scrape_details.html', tdata)

def list_classes(request):
    clist = Class.objects.all().order_by('-enrollware_id')
    tdata = {'classes': []}
    for c in clist:
        r = Registration.objects.filter(class_pk=c).count()
        tdata['classes'].append((c, r))
    
    return render_to_response('ewatch/list_classes.html', tdata)
