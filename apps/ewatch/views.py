from django.shortcuts import render_to_response

from apps.ewatch.models import Class, Registration

def index(request):
    return render_to_response('ewatch/base.html')

def list_classes(request):
    clist = Class.objects.all().order_by('-enrollware_id')
    tdata = {'classes': []}
    for c in clist:
        r = Registration.objects.filter(class_pk=c).count()
        tdata['classes'].append((c, r))
    
    return render_to_response('ewatch/list_classes.html', tdata)
