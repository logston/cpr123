from bs4 import BeautifulSoup

class FetchRegistrationParser():
    """A class that defines methods for parsing html for registration data"""

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html)
        self.registration_edit_table = None
        
    def _get_registration_edit_table(self, soup):
        if not self.registration_edit_table:
            tables = []
            for table in self.soup.find_all('table'):
                if 'id' in table.attrs and \
                        table['id'] == 'mainContent_certType':
                    continue
                tables.append(table)
            table_0 = tables[0] if tables else None
            self.registration_edit_table = table_0
        return self.registration_edit_table

    def _get_select_tag_values(self, selects):
        """Return a dict with every select's info"""
        select_details = {}
        for select in selects:
            attrs = select.attrs
            keys = attrs.keys()
            if 'id' in keys and attrs['id'] == 'mainContent_reschedSelect':
                # reschedule_class FK to class
                select_details['reschedule_class']=\
                        self._get_selected_option(select, True)
            elif 'id' in keys and attrs['id']=='mainContent_StateSelect':
                # mailing state
                select_details['mailing_state']=\
                        self._get_selected_option(select, True)
            elif 'id' in keys and attrs['id']=='mainContent_billingState':
                # billing state
                select_details['billing_state']=\
                        self._get_selected_option(select, True)
            elif 'id' in keys and attrs['id']=='mainContent_promoCode':
                # promo code
                select_details['promo_code']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id']=='mainContent_bookSelect':
                # book
                select_details['book']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id']=='mainContent_status':
                # status
                select_details['status']=self._get_selected_option(select)
            elif 'id' in keys and attrs['id']=='mainContent_remediationSelect':
                # remediation_scheduled
                select_details['remediation_scheduled']=\
                        self._get_selected_option(select, True)
        return select_details
    
    def _get_selected_option(self, select, value=False):
        for op in select.find_all('option'):
            try:
                op['selected']
                if value:
                    return str(op['value'])
                else:
                    return str(op.string)
            except KeyError:
                pass
    
    def get_details_dict(self, table):
        details = {}
        details['mailing'] = {}
        details['billing'] = {}
        selects = table.find_all('select')
        if selects:
            details.update(self._get_select_tag_values(selects))
        if 'mailing_state' in details.keys():
            details['mailing']['state'] = details['mailing_state']
            del(details['mailing_state'])
        if 'billing_state' in details.keys():
            details['billing']['state'] = details['billing_state']
            del(details['billing_state'])
        inputs = table.find_all('input')
        for i in inputs:
            attrs = i.attrs
            keys = attrs.keys()
            if not 'id' in keys:
                continue
            if attrs['id'] == 'mainContent_certType_0':
                # cert_type / Certification
                if 'checked' in keys and attrs['checked'] == 'checked':
                    details['cert_type'] = 'C'
            if attrs['id'] == 'mainContent_certType_1':
                # cert_type / Recertification
                if 'checked' in keys and attrs['checked'] == 'checked':
                    details['cert_type'] = 'R'
            if attrs['id'] == 'mainContent_checkedIn':
                # checked_in
                if 'checked' in keys and attrs['checked'] == 'checked':
                    details['checked_in'] = True
                else:
                    details['checked_in'] = False
            if not 'value' in keys:
                continue
            if attrs['id'] == 'mainContent_fnameTextBox':
                # first_name
                details['first_name'] = i['value']
            if attrs['id'] == 'mainContent_lnameTextBox':
                # last_name
                details['last_name'] = i['value']
            if attrs['id'] == 'mainContent_emailTextBox':
                # email_address
                details['email_address'] = i['value']
            if attrs['id'] == 'mainContent_primaryPhone':
                # primary_phone
                details['primary_phone'] = i['value']
            if attrs['id'] == 'mainContent_alternatePhone':
                # alternate_phone
                details['alternate_phone'] = i['value']
            if attrs['id'] == 'mainContent_Addr1TextBox':
                # mailing_address 1
                details['mailing']['address_1'] = i['value']
            if attrs['id'] == 'mainContent_Addr2TextBox':
                # mailing_address 2
                details['mailing']['address_2'] = i['value']
            if attrs['id'] == 'mainContent_CityTextBox':
                # mailing_city
                details['mailing']['city'] = i['value']
            if attrs['id'] == 'mainContent_ZipTextBox':
                # mailing_zip
                details['mailing']['zip'] = i['value']
            if attrs['id'] == 'mainContent_billingAddress1':
                # billing_address 1
                details['billing']['address_1'] = i['value']
            if attrs['id'] == 'mainContent_billingAddress2':
                # billing_address 2
                details['billing']['address_2'] = i['value']
            if attrs['id'] == 'mainContent_billingCity':
                 # billing_city
                 details['billing']['city'] = i['value']
            if attrs['id'] == 'mainContent_billingZip':
                # billing_zip
                details['billing']['zip'] = i['value']
            if attrs['id'] == 'mainContent_bookShippedDate':
                # book_pickup_date
                details['book_pickup_date'] = i['value']
            if attrs['id'] == 'mainContent_totalCharge':
                # total_charge
                details['total_charge'] = i['value']
            if attrs['id'] == 'mainContent_code':
                # codes
                details['codes'] = i['value']
            if attrs['id'] == 'mainContent_testScore':
                # test_score
                details['test_score'] = i['value']
        trs = table.find_all('tr')
        for tr in trs:
            if not tr.th:
                continue
            if tr.th.string and 'Certificate #:' in tr.th.string:
                # certificate_number
                i = tr.find('input', id='mainContent_testScore')
                if i.has_attr('value'):
                    details['certificate_number'] = i['value']
                    del(details['test_score'])
            if tr.th.string == 'How did you hear about us?':
                # hear
                details['hear'] = tr.td.string
            if tr.th.string == 'Have you taken a course with us at CPR123?':
                # return_client
                details['return_client'] = tr.td.string
        textareas = table.find_all('textarea')
        for textarea in textareas:
            if 'id' in textarea.attrs.keys() and \
                    textarea['id'] == 'mainContent_commentText':
                # comments
                details['comments'] = textarea.string.strip()
        return details

    def get_all_registration_info(self):
        t = self._get_registration_edit_table(self.soup)
        if not t:
            return {}
        details = self.get_details_dict(t)
        return details 
