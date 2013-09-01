from datetime import timedelta
from decimal import Decimal

from django.shortcuts import render_to_response

from apps.ewatch.models import *
from libs.ref.timezones import UTC

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
    
    # for all classes, get distinct years/months in those classes
    dts = Class.objects.dates('time', 'month', order='DESC')
    c['months'] = [(dt.year, dt.month) for dt in dts]
    
    # for all months, get class count
    c['class_count'] = {}
    for mo in c['months']:
        c['class_count'][mo] = Class.objects.filter(time__year=mo[0]).\
            filter(time__month=mo[1]).count()
    
    return render_to_response('ewatch/tally_classes.html', c)


def tally_regs(request):
    c = {}
    return render_to_response('ewatch/tally_regs.html', c)


def tally_revenue(request):
    c = {}
    # given month/year and location return revenue

    loc_MN = Location.objects.get(name='Manhattan')
    loc_LI = Location.objects.get(name='Long Island')
    loc_KG = Location.objects.get(name='Queens Kew Gardens')
    locs = (loc_MN, loc_LI, loc_KG)

    # for all classes, get distinct years/months in those classes
    dts = Class.objects.dates('time', 'month', order='DESC')

    c['stats_by_month_and_loc'] = []
    for dt in dts:
        loc_stats = []
        # this line is a hack to get months to show up correctly
        dt = dt.astimezone(UTC()) + timedelta(hours=6)
        for loc in locs:
            regs = Registration.objects.\
                filter(class_pk__time__year=dt.year).\
                filter(class_pk__time__month=dt.month).\
                filter(class_pk__location=loc)
            loc_stats.append(
                sum([reg.total_charge for reg in regs if reg.total_charge]))
        c['stats_by_month_and_loc'].append((dt,loc_stats))

    return render_to_response('ewatch/tally_revenue.html', c)