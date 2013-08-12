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
import sys

from django.db.utils import IntegrityError
from django.utils import timezone
from apps.ewatch.models import Class 

# add an import to get username and password for enrollware
from priv.enrollware_password import enrollware_password
from priv.enrollware_username import enrollware_username
from priv.cookiejar_file_path import cookiejar_file_path

from libs.fetch.fetchpastclasses import FetchPastClasses
from libs.fetch.fetchparser import FetchParser

class_list = Class.objects.filter(time__lt=timezone.now())
db_id_list = [class_.enrollware_id for class_ in class_list]

print(len(db_id_list), ' class objects found in database')

START_DATE_STR = '12/01/2009'
fetcher = FetchPastClasses(cookiejar_file_path)
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
        class_obj.removed = True
        class_obj.save()
        cntr += 1
print(cntr, " class objects updated to 'removed'")

cntr = 0
# create new classes
for class_id in fetched_id_list:
    if class_id not in db_id_list:
        try:
            Class.objects.create(enrollware_id=class_id)
            cntr += 1
        except IntegrityError:
            pass
print(cntr, " class objects added to database")
