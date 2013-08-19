"""
This module is to be run as an updater for the db.

It requests a list of all past classes in the time interval
4 weeks from today to 1 week from today. 

It first finds all class ids in the db and checks to see
if they are also in the search.
It then checks to see if any new class id are not already in the db and then
inserts them as necessary.
"""

from datetime import datetime
from datetime import timedelta

from django.db.utils import IntegrityError
from django.utils import timezone
from apps.ewatch.models import Class 

from apps.ewatch.fetch.fetchpastclasses import FetchPastClasses
from apps.ewatch.fetch.fetchparser import FetchParser
from libs.ref.timezones import EST

def update_past_months_class_ids():
    """Return nothing after updating past class ids"""
    class_list = Class.objects.filter(time__lte=timezone.now())
    print(class_list.count(), ' class objects found in database')
    db_id_list = [class_.enrollware_id for class_ in class_list]

    print(len(db_id_list), ' class ids retrieved from database')

    start_date = datetime.now(EST()) + timedelta(days=-30)
    end_date = datetime.now(EST()) + timedelta(days=-7)

    fetcher = FetchPastClasses()
    html = fetcher.fetch_between(
        start_date=start_date,
        end_date=end_date)
    parser = FetchParser(html)
    fetched_id_list = parser.get_class_id_list_from_class_list()

    print(len(fetched_id_list), ' class objects found on enrollware')

    cntr = 0
    # create new classes
    for class_id in fetched_id_list:
        if class_id not in db_id_list:
            try:
                Class.objects.create(enrollware_id=class_id, removed=False)
                cntr += 1
            except IntegrityError:
                pass
    print(cntr, " class objects added to database")

if __name__ == '__main__':
    update_past_months_class_ids()
