from apps.ewatch.fetch.fetch import Fetch
from apps.ewatch.fetch.fetchparser import FetchParser

class FetchClass(Fetch):
    """A class for fetching class details and registration ids/times"""
    
    def fetch_class(self, class_id):
        """Fetch class details and registration ids/times"""
        action = '/admin/class-edit1.aspx?ret=class-list.aspx&id=' + \
                str(class_id)
        response = self.make_request(action)
        parser = FetchParser(response.read())
        return parser.get_all_class_info()
