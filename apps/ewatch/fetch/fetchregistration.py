from apps.ewatch.fetch.fetch import Fetch
from apps.ewatch.fetch.fetchregistrationparser import FetchRegistrationParser

class FetchRegistration(Fetch):
    """A class for fetch registration details from enrollware"""
    
    def fetch_registration(self, class_id, registration_id):
        """Fetch registration details from enrollware"""
        action = '/admin/class-registration-edit.aspx?id='+ \
                 str(registration_id)+'&'+'classSchedId='+str(class_id)
        response = self.make_request(action)
        parser = FetchRegistrationParser(response.read())
        return parser.get_all_registration_info()
