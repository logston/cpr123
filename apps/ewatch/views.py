from collections import Counter
from datetime import timedelta
from decimal import Decimal
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.ewatch.models import *
from libs.api.google_geocode import get_lat_long
from libs.ref.timezones import UTC
from libs.utils.validators import is_valid_zip as is_valid_zip

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def index(request):
    c = RequestContext(request, {})
    return render_to_response('ewatch/index.html', c)

@login_required
def scrape_details(request):
    c = RequestContext(request, {})
    c['last_fetch'] = UpdateCheckClass.objects.order_by('-time').all()[0].time
    c['last_class'] = Class.objects.order_by('-time').all()[0].time

    # percent of past classes scraped
    classes_scraped = set(UpdateCheckClass.objects.
                     values_list('class_pk__enrollware_id', flat=True))
    # set the list so duplicates are removed
    c['classes_scraped'] = len(classes_scraped)
    c['total_classes'] = Class.objects.all().count()
    c['percent_classes_scraped'] = round(
        (c['classes_scraped']/c['total_classes']) * 100)


    c['days_till_complete_coverage'] = round((c['total_classes'] - 
        c['classes_scraped']) / 180, 2)
    
    # percent of class scrapes succuessful (ie. has course name)
    c['classes_scrape_success'] = (Class.objects.
                                   exclude(course='').
                                   exclude(course=None).
                                   count())
    c['percent_classes_scrape_success'] = round(
        (c['classes_scrape_success']/c['classes_scraped']) * 100)
            
    # percent of registrations scrapes sucuessful (ie. has name)
    qset = (UpdateCheckRegistration.objects.
            exclude(registration_pk__total_charge=None))
    c['regs_scraped'] = len(set(
        [q.registration_pk.enrollware_id for q in qset]))
    c['regs_scraped_success'] = (Registration.objects.
                                 exclude(total_charge=None).
                                 count())
    c['percent_regs_scrape_success'] = (round(
        (c['regs_scraped_success']/c['regs_scraped']) * 100))
    
    return render_to_response('ewatch/scrape_details.html', c)

def main_locations():
    loc_MN = Location.objects.get(name='Manhattan')
    loc_LI = Location.objects.get(name='Long Island')
    loc_KG = Location.objects.get(name='Queens Kew Gardens')
    return (loc_MN, loc_LI, loc_KG)

@login_required
def tally_classes(request):
    c = RequestContext(request, {})

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
                tally = (Class.objects.
                         filter(time__year=dt.year).
                         filter(time__month=dt.month).
                         filter(course=course_tallies[0]).
                         filter(location=loc).count())
                course_tallies.append(tally)
            if sum(course_tallies[1:]):
                stats_by_month_and_loc.append(course_tallies)
        c['class_tallies_by_month_and_loc'].append([dt, sorted(stats_by_month_and_loc)])
    
    return render_to_response('ewatch/tally_classes.html', c)

@login_required
def tally_classes2(request):
    c = RequestContext(request, {})

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

@login_required
def tally_revenue(request):
    c = RequestContext(request, {})

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
            regs = (Registration.objects.
                    filter(class_pk__time__year=dt.year).
                    filter(class_pk__time__month=dt.month).
                    filter(class_pk__location=loc))
            loc_stats.append(
                sum([reg.total_charge for reg in regs if reg.total_charge]))
        c['stats_by_month_and_loc'].append((dt,loc_stats))

    return render_to_response('ewatch/tally_revenue.html', c)

@login_required
def heatmap(request):
    c = RequestContext(request, {})
    reg_mail_zips = Registration.objects.values('mailing_address__zip_code')
    mailing_zips = [zcD['mailing_address__zip_code'][:5] 
                    for zcD in reg_mail_zips if 
                    zcD['mailing_address__zip_code'] and 
                    is_valid_zip(zcD['mailing_address__zip_code'][:5])]
    zip_counter = Counter(mailing_zips).most_common(200)
    #mcz_count = zip_counter.most_common(1)[0][1]
    #zip_relative_probabi = [(zc, round((cnt/mcz_count), 3)) for zc, cnt in zip_counter.items()]
    llData = []
    for zc, cnt in zip_counter:
        ll = get_lat_long(zc)
        for x in range(cnt):
            llData.append(ll)
    llStrs = []
    for ll in llData:
        llStrs.append('new google.maps.LatLng('+str(ll[0])+', '+str(ll[1])+')')

    #c['llStr'] = ','.join(llStrs[:200])
    c['lats_longs'] = llData

    return render_to_response('ewatch/heatmap.html', c)

@login_required
def dist_of_reg_times(request):
    c = RequestContext(request, {})
    return render_to_response('ewatch/dist_of_reg_times.html', c)

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

"""
Ideas on handing figures to templates.

Images should be rendered to ImageField objects and handed back to 
the view requesting them for display.

Figures should have their own urls and should be rendered via
their own individual views. The urls of those views should be
inserted into templates. Issue with this is rerednering previously
rendered stuff. Also the urls are liable to change often given
what it represents.
For smaller projects with few figures I think this is the better 
option. 

"""
def dist_of_reg_times_fig(request):
    times_queryset = Registration.objects.values('class_pk__time', 'registration_time')

    tdeltas = ([t['class_pk__time'] - t['registration_time'] 
                for t in times_queryset if t['registration_time']])

    tdeltas = [t.total_seconds()/(24*60*60) for t in tdeltas]

    fig = Figure(figsize=[8,8])
    ax = fig.add_subplot(1,1,1)
    canvas = FigureCanvasAgg(fig)

    bins = range(-10,60,1)
    n, bins, patches = ax.hist(tdeltas, bins, normed=1, facecolor='green', alpha=0.5)

    ax.set_xlabel('Days in advance of class')
    ax.set_ylabel('Fraction of Registrations')
    ax.set_title('Registrations Times')

    response = HttpResponse(content_type='image/png')
    canvas.print_figure(response, facecolor='w')

    return response
