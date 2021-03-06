"""
This model defines a function that:
0.  Will only run between 9am and 6pm 
1.  finds Class records (starting from most recent occuring based on 
    enrollware_id) in db with no or longest ago UpdateChecks
2.  Waits a random number of seconds to simulate a user
3.  Updates Class
4.  Update Registrations associated with that Class
5.  For each Registration, wait a random number of seconds (3, 8) 
    in between each UpdateRegistration call
"""

from datetime import datetime
from datetime import timedelta
import random
import sys
import time

from django.utils import timezone

from apps.ewatch.models import Class, Registration
from apps.ewatch.models import UpdateCheckClass, UpdateCheckRegistration

from apps.ewatch.db.updateclass import UpdateClass
from apps.ewatch.db.updateregistration import UpdateRegistration
from libs.ref.timezones import EST

def is_working_hours(manual_override=False):
    if manual_override:
        return True
    dt = datetime.now(EST())
    wd = dt.weekday()
    hr = dt.hour
    if (hr>=9 and hr<18) and (wd>=0 and wd<=4):
        return True
    return False

def update_class_and_registrations(enrollware_class_id=None, 
                                   manual_override=False):
    """Finds next Class valid for updating and updates it"""
    if not enrollware_class_id:
        updates = UpdateCheckClass.objects.order_by('-time').all()
        if updates and updates[0].exception == True:
            # immediatley exit since last update failed
            sys.exit(1)
        updated_class_pks = []
        # find a list of updated classes
        for update in updates:
            if not update.class_pk in updated_class_pks:
                updated_class_pks.append(update.class_pk)
        all_classes = Class.objects.order_by('-enrollware_id').all()
        
        if len(updated_class_pks) == all_classes.count():
            # all classes have an update, exit
            return sys.exit(0)
        else:
            # some un updated Classes left, grab most recent unupdate one
            for class_ in all_classes:
                if not class_ in updated_class_pks:
                    enrollware_class_id = class_.enrollware_id
                    break
         
    time.sleep(random.random()*15) # sleep for a random number of seconds
    
    try:
        class_ = UpdateClass(enrollware_class_id).update()
        #class_ = Class.objects.get(enrollware_id=enrollware_class_id)
        registrations = Registration.objects.filter(class_pk=class_)
        for reg in registrations:
            time.sleep(random.random()*5+3)
            UpdateRegistration(enrollware_class_id, reg.enrollware_id).update()
        
        UpdateCheckClass.objects.create(class_pk=class_, exception=False)
    except Exception as e:
        # make note of the updates that have occured
        UpdateCheckClass.objects.create(class_pk=class_, exception=True)
        raise e


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'manual':
        update_class_and_registrations()
        sys.exit(0)
    if len(sys.argv) == 2:
        update_class_and_registrations(sys.argv[1], True) 
        sys.exit(0)
    if is_working_hours():
        update_class_and_registrations()
    else:
        sys.exit(0)
