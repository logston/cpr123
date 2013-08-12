import urllib.parse

from bs4 import BeautifulSoup

class FetchParser():
    def __init__(self, html):
        self.html = html
        
    def get_class_id_list_from_class_list(self):
        """Return list of class ids"""
        soup = BeautifulSoup(self.html)
        tr_list = soup.find(
                id='main-content'
                ).table.tbody.find_all('tr')
        href_list = []
        for tr in tr_list:
            qs = urllib.parse.urlparse(tr.find(title='Edit')['href'])[4]
            id_ = urllib.parse.parse_qs(qs)['id'][0]
            href_list.append(id_)
        return href_list
