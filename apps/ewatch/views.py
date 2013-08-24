from django.shortcuts import render_to_response

from apps.ewatch.models import *

def index(request):
    return render_to_response('ewatch/index.html')

def scrape_details(request):
    tdata = {}
    # percent of past classes scraped
    scraped_c = UpdateCheckClass.objects.values_list('class_pk', flat=True)    
    # set the list so duplicates are removed
    tdata['classes_scraped'] = len(set(scraped_c))
    tdata['total_classes'] = Class.objects.all().count()
    tdata['percent_classes_scraped'] = \
        round((tdata['classes_scraped']/tdata['total_classes'])*100)
    
    # percent of class scrapes succuessful (ie. has course name)
    tdata['classes_scrape_success'] = \
        Class.objects.exclude(course='').exclude(course=None).count()
    tdata['percent_classes_scrape_success'] = \
        round((tdata['classes_scrape_success']/tdata['classes_scraped']) * 100)
            
    # percent of registrations scrapes sucuessful (ie. has name)
    tdata['regs_scraped'] = UpdateCheckRegistration.objects.all().count()
    tdata['regs_scraped_success'] = \
        Registration.objects.\
            exclude(total_charge=None).\
            count()
    tdata['percent_regs_scrape_success'] = \
        round((tdata['regs_scraped_success']/tdata['regs_scraped']) * 100)
    
    return render_to_response('ewatch/scrape_details.html', tdata)

def tally_classes(request):
    c = {}

    return render_to_response('ewatch/tally_classes.html', c)

def tally_regs(request):
    c = {}
    return render_to_response('ewatch/tally_regs.html', c)

def tally_revenue(request):
    c = {}
    # given month/year and location return revenue
    # mulit line (locatino) plot
    # year-month 

    # for all classes get distinct years of classes

    # for all years, get distinct months in those classes

    # for all months, get 4 locations

    # for all locations, get registrations

    # for all registrations, get list revenue totals

    loc_MN = Location.objects.get(name='Manhattan')
    loc_LI = Location.objects.get(name='Long Island')
    loc_KG = Location.objects.get(name='Queens Kew Gardens')




    return render_to_response('ewatch/tally_revenue.html', c)