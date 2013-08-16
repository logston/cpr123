import http.cookiejar
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from priv.cookiejar_file_path import cookiejar_file_path
from priv.enrollware_password import enrollware_password
from priv.enrollware_username import enrollware_username

class Fetch():
    """Make URL requests with cookies in cookiejar"""

    def __init__(self, cookiejar_file=cookiejar_file_path):
        self.origin = 'https://www.enrollware.com/'
        self.cj = http.cookiejar.LWPCookieJar(cookiejar_file)
        try:    
            self.cj.load()
        except:
            self.cj.save()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj))

    def make_request(self, action, data=None):
        """Return html of request"""
        response = self.call_opener(action, data)
        if '/admin/login.aspx' in response.geturl():
            # client has be rerouted to login
            login_response = self.login(response)
            response_parse = urllib.parse.urlparse(response.geturl())
            login_parse = urllib.parse.urlparse(login_response.geturl())
            if response_parse[2] == login_parse[2]: 
                # still on login page
                return response  
            else:
                # retry request once more
                return self.call_opener(action, data)
        else:
            return response

    def call_opener(self, action, data=None):
        url = urllib.parse.urljoin(self.origin, action)
        #print('requesting ' + url)
        request = urllib.request.Request(url)
        if data:
            data = urllib.parse.urlencode(data).encode('utf-8')
            request.add_header(
                "Content-Type",
                "application/x-www-form-urlencoded;charset=utf-8")
        try:
            return self.opener.open(request, data)
        except Exception as e:
            raise e 

    def login(self, response):
        """Login"""
        soup = BeautifulSoup(response.read())
        data = self.get_login_post_data(soup)
        action = self.get_login_post_action(soup)
        response = self.call_opener(action, data)
        self.cj.save()
        return response

    def get_login_post_data(self, soup):
        """Return utf-8 encoded data for use in post"""
        data = []
        for i in soup.find_all('input'):
            name = i['name']
            if name == 'username':
                data.append((name, enrollware_username))
            elif name == 'password':
                data.append((name, enrollware_password))
            elif name == 'rememberMe':
                data.append((name, 'on'))
            else:
                data.append((name, i['value']))
        return data

    def get_login_post_action(self, soup):
        """Return the post action"""
        return soup.find(id="form1")['action']
