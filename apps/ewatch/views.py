from collections import Counter
from datetime import timedelta
from decimal import Decimal
import logging

from django.shortcuts import render_to_response

from apps.ewatch.models import *
from libs.api.google_geocode import get_lat_long
from libs.ref.timezones import UTC
from libs.utils.validators import is_valid_zip as is_valid_zip

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def index(request):
    return render_to_response('ewatch/index.html')

def scrape_details(request):
    tdata = {}

    tdata['last_class'] = Class.objects.order_by('-time').all()[0].time

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

def main_locations():
    loc_MN = Location.objects.get(name='Manhattan')
    loc_LI = Location.objects.get(name='Long Island')
    loc_KG = Location.objects.get(name='Queens Kew Gardens')
    return (loc_MN, loc_LI, loc_KG)

def tally_classes(request):
    c = {}

    c['last_class'] = Class.objects.order_by('-time').all()[0].time

    locs = main_locations()
    
    # for all classes, get distinct years/months in those classes
    dts = Class.objects.dates('time', 'month', order='DESC')
    # for all classse, get distinct course types
    courses = Class.objects.values('course').distinct()
    
    c['class_tallies_by_month_and_loc'] = []
    for dt in dts:
        # this line is a hack to get months to show up correctly
        dt = dt.astimezone(UTC()) + timedelta(hours=6)
        stats_by_month_and_loc = []
        for course in courses:
            course_tallies = [course['course'].replace('â\x84¢', '')]
            for loc in locs:
                tally = Class.objects.\
                    filter(time__year=dt.year).\
                    filter(time__month=dt.month).\
                    filter(course=course_tallies[0]).\
                    filter(location=loc).count()
                course_tallies.append(tally)
            if sum(course_tallies[1:]):
                stats_by_month_and_loc.append(course_tallies)
        c['class_tallies_by_month_and_loc'].append([dt, sorted(stats_by_month_and_loc)])
    
    return render_to_response('ewatch/tally_classes.html', c)

def tally_classes2(request):
    c = {}

    c['last_fetch'] = UpdateCheckClass.objects.order_by('-time').all()[0].time
    c['last_class'] = Class.objects.order_by('-time').all()[0].time

    locs = main_locations()

    classes = [class_ for class_ in Class.objects.all()]
    
    # for all classes, get distinct years/months in those classes
    dts = Class.objects.dates('time', 'month', order='DESC')
    # for all classse, get distinct course types
    courses = Class.objects.values('course').distinct()
    
    c['class_tallies_by_month_and_loc'] = []
    for dt in dts:
        # this line is a hack to get months to show up correctly
        dt = dt.astimezone(UTC()) + timedelta(hours=6)
        
        stats_by_month_and_loc = []
        for course in courses:
            course_tallies = [course['course'].replace('â\x84¢', '')]
            for loc in locs:
                # count classes that qualify
                course_tallies.append(loc_tally(classes, dt, course['course'], loc))
            if sum(course_tallies[1:]):
                stats_by_month_and_loc.append(course_tallies)
        c['class_tallies_by_month_and_loc'].append([dt, sorted(stats_by_month_and_loc)])
    
    return render_to_response('ewatch/tally_classes.html', c)

def loc_tally(classes, dt, course, loc):
    if not classes or not dt or not course or not loc:
        return 0
    cnt = 0
    for class_ in classes:
        if not class_ or not class_.time or not class_.course or not class_.location:
            continue
        if not dt.year == class_.time.year:
            continue
        if not dt.month == class_.time.month:
            continue
        if not course == class_.course:
            continue
        if not loc == class_.location:
            continue
        cnt += 1
    return cnt


def tally_revenue(request):
    c = {}

    c['last_fetch'] = UpdateCheckClass.objects.order_by('-time').all()[0].time
    c['last_class'] = Class.objects.order_by('-time').all()[0].time
    
    # given month/year and location return revenue
    locs = main_locations()

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

def heatmap(request):
    c = {}
    reg_mail_zips = Registration.objects.values('mailing_address__zip_code')
    mailing_zips = [zcD['mailing_address__zip_code'][:5] for zcD in \
        reg_mail_zips if zcD['mailing_address__zip_code'] and \
        is_valid_zip(zcD['mailing_address__zip_code'][:5])]
    zip_counter = Counter(mailing_zips)
    #mcz_count = zip_counter.most_common(1)[0][1]
    #zip_relative_probabi = [(zc, round((cnt/mcz_count), 3)) for zc, cnt in zip_counter.items()]
    j = [get_lat_long(zc) for zc, cnt in zip_counter.items()]
    c['mailing_zips'] = j
    return render_to_response('ewatch/heatmap.html', c)


