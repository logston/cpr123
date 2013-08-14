from decimal import *

from apps.ewatch.models import Class, Instructor, Location

class ConditionClassFetch():
    """
    A class with a number of methods for conditioning fetched 
    class data for the database
    """
    
    def __init__(self):
        pass

    def class_registration(self, reg):
        """Return a db ready 2-tup (reg_id, reg_datetime)"""
        return (int(reg[0]), reg[1])
    
    def class_registrations(self, reg_list):
        """Return a db ready list of registrations"""
        db_reg_list = []
        for reg in reg_list:
            db_reg_list.append(self.class_registration(reg))
        return db_reg_list

    def class_details(self, din):
        """Return a db ready dictionary of class details"""
        dout = {}
        if 'course' in din:
            dout['course'] = din['course']
        if 'registration_link' in din:
            dout['registration_link'] = din['registration_link']
        if 'bulk_registration_link' in din:
            dout['bulk_registration_link'] = din['bulk_registration_link']
        if 'client' in din:
            dout['client'] = din['client']
        if 'location' in din:
            try:
                dout['location'] = Location.objects.get(name=din['location'])
            except:
                dout['location'] = din['location']
        if 'instructor' in din: 
            i = din['instructor'].split()
            i_list = Instructor.objects.filter(first_name__icontains=i[0])
            for instructor in i_list:
                if instructor.last_name == ' '.join(i[1:]):
                    dout['instructor'] = instructor
        if 'time' in din:
            dout['time'] = din['time']
        if 'max_students' in din:
            dout['max_students'] = int(din['max_students'])
        if 'max_students_link' in din:
            try:
                # get pk for other class
                c = Class.objects.get(
                        enrollware_id=int(din['max_students_link']))
            except:
                # or get ready to add anther
                c = int(din['max_students_link'])
            dout['max_students_link'] = c
        if 'listing' in din:
            dout['listing'] = True if din['listing'] == 'checked' else False
        if 'price' in din:
            dout['price'] = Decimal(din['price'])
        if 'book_price' in din:
            dout['book_price'] = Decimal(din['book_price'])
        if 'student_manikin_ratio' in din:
            dout['student_manikin_ratio'] = int(
                    din['student_manikin_ratio'].split(':')[0])
        if 'total_hours' in din and din['total_hours']:
            dout['total_hours'] = int(din['total_hours'])  
        return dout
