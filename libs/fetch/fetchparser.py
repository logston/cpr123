from datetime import datetime
import re
import urllib.parse

from bs4 import BeautifulSoup

class FetchParser():
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html)
        self.class_edit_tables = None

    def get_class_id_list_from_class_list(self):
        """Return list of class ids"""
        tr_list = self.soup.find(
                id='main-content'
                ).table.tbody.find_all('tr')
        href_list = []
        for tr in tr_list:
            qs = urllib.parse.urlparse(tr.find(title='Edit')['href'])[4]
            id_ = urllib.parse.parse_qs(qs)['id'][0]
            href_list.append(id_)
        return href_list

    def _get_class_edit_tables(self, soup):
        if not self.class_edit_tables:
            self.class_edit_tables = soup.find_all('table')
        return self.class_edit_tables

    def _get_select_tag_values(self, selects):
        """Return a dict with every select's info"""
        select_details = {}
        for select in selects:
            attrs = select.attrs
            keys = attrs.keys()
            if 'id' in keys and attrs['id'] == 'mainContent_Course':
                # course
                select_details['course']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id'] == 'mainContent_tsclientId':
                # client
                select_details['client']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id'] == 'mainContent_Location':
                # location
                select_details['location']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id'] == 'mainContent_instructorId':
                # instructor
                select_details['instructor']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id'] == 'mainContent_manikinRatio':
                # student_manikin_ratio
                select_details[
                        'student_manikin_ratio']=self._get_selected_option(
                                select)
        return select_details

    def _get_selected_option(self, select):
        for op in select.find_all('option'):
            try:
                op['selected']
                return op.string
            except KeyError:
                pass

    def _get_class_time(self, html):
        """Return an aware datetime instance"""
        sliver = str(html).split('mainContent_studentPanel')[1].split(
                'mainContent_addStudentLink')[0].split(
                '<h3>')[1].split('</h3>')[0]
        time_str = sliver.split('-')[1].strip()
        #time_str = sliver.split('-')[1].strip().strip(r'\\r\\n')
        patt = r'.*, (\S*) (\d+), (\d+) at (\d+):(\d+) ([A|P]M).*'
        r = re.match(patt, time_str, re.DOTALL)
        g = r.groups()
        day = str(g[1]) if len(g[1]) == 2 else str('0'+g[1])
        hour = str(g[3]) if len(g[3]) == 2 else str('0'+g[3])
        datetime_list = (g[0], day, g[2], hour, g[4], g[5])
        datetime_str = ' '.join(datetime_list)
        return datetime.strptime(datetime_str, '%B %d %Y %I %M %p')

    def get_details_dict_from_class_id(self):
        """Return a dictionary of class details"""
        tbody = self._get_class_edit_tables(self.soup)[1]
        details = {}
        for tr in tbody.find_all('tr'):
            selects = tr.find_all('select')
            if selects:
                # handle selects seperately
                details.update(self._get_select_tag_values(selects))
            if tr.find(id='mainContent_directLink'):
                # Registratoin link
                details['registration_link'] = tr.a.string
            if tr.find(id='mainContent_bulkLink'):
                # bulk_registration_link
                details['bulk_registration_link'] = tr.a.string
            if tr.find(id='mainContent_price'):
                # price
                details['price'] = tr.input['value'].strip('$')
            if tr.find(id='mainContent_bookPrice'):
                # book price
                details['book_price'] = tr.input['value'].strip('$')
            if tr.find(id='mainContent_maxEnrollment'):
                # max students
                details['max_students'] = tr.input['value']
            if tr.find(id='mainContent_listOnline'):
                # listing on online catalogue
                input_ = tr.find(id='mainContent_listOnline')
                details['listing'] = input_.get('checked')
            if tr.find(id='mainContent_totalHours'):
                # total_hours
                input_ = tr.find(id='mainContent_totalHours')
                details['total_hours'] = input_.get('value')
        details['time']=self._get_class_time(self.html)
        return details

    def get_registration_ids_and_times(self):
        """Return a list of tuples of reg ids and times"""
        tbody = self._get_class_edit_tables(self.soup)[0].tbody
        return len(tbody.find_all('tr'))

    def get_all_class_info(self):
        details = self.get_details_dict_from_class_id()
        regis = self.get_registration_ids_and_times()
        return {'registrations':regis, 'details':details}
