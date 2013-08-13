"""
2013 Paul Logston
"""
from datetime import datetime
import time

from bs4 import BeautifulSoup

from libs.fetch.fetch import Fetch

class FetchPastClasses(Fetch):
    """Get past classes within interval"""
    
    past_classes_url = '/admin/past-classes.aspx'

    def fetch_between(self, start_date, end_date=datetime.today()):
        """Return past classes html"""
        # first make call to /admin/past-classes.apsx to get current inputs
        response = self.make_request(self.past_classes_url)
        response_html = response.read()
        data = self.get_inputs(response_html)

        date_format = '%m/%d/%Y'
        # if data show that the first request covers needs, return response
        sdate_cj = datetime.strptime(
                data['ctl00$mainContent$sdate'], date_format)
        edate_cj = datetime.strptime(
                data['ctl00$mainContent$edate'], date_format)
        
        if start_date >= sdate_cj and end_date <= edate_cj:
            #request satisfied. No second request made
            return response_html

        # change given datetimes into fomatted strings.
        sdate_str = start_date.strftime(date_format)
        edate_str = end_date.strftime(date_format)
        
        # override some of the data
        data['ctl00$mainContent$sdate'] = sdate_str
        data['ctl00$mainContent$edate'] = edate_str

        # sleep for two seconds to mimic human navigating site
        time.sleep(2)

        response = self.make_request(self.past_classes_url, data)
        return response.read()
        
    def get_inputs(self, html):
        """Return inputs and values from response html in dict"""
        data = {}
        for i in BeautifulSoup(html).find_all('input'):
            data[i['name']] = i['value']
        return data
