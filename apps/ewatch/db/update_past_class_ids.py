"""
This module is to be run as an updater for the db.

It requests a list of all past classes since Tue 12/01/09 1:00p EST.
If first finds all class ids in the db and checks to see
if they are also in the search. If one is not, the db is updated to show 
that the class was removed.
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


def update_past_class_ids():
    """Return nothing after updating past class ids"""
    class_list = Class.objects.filter(time__lte=timezone.now())
    print(class_list.count(), ' class objects found in database')
    db_id_list = [class_.enrollware_id for class_ in class_list]

    print(len(db_id_list), ' class ids retrieved from database')

    START_DATE_STR = '12/01/2009'
    fetcher = FetchPastClasses()
    html = fetcher.fetch_between(
        start_date=datetime.strptime(START_DATE_STR,'%m/%d/%Y'),
        end_date=timezone.now())
    parser = FetchParser(html)
    fetched_id_list = parser.get_class_id_list_from_class_list()

    print(len(fetched_id_list), ' class objects found on enrollware')

    # mark removed classes
    cntr = 0
    for class_id in db_id_list:
        if class_id not in fetched_id_list:
            # class id is no longer in list of ids from enrollware
            class_obj = Class.objects.get(enrollware_id=class_id)
            # following lines give incorrect results if module
            # is run with any future classes in db, this is a past class mod 
            #class_obj.removed = True
            #class_obj.save()
            #cntr += 1
    print(cntr, " class objects updated to 'removed'")

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
    update_past_class_ids()
