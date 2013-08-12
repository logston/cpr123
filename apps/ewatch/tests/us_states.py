from django.test import TestCase

from libs.us_states import us_states

class TestUSStatesModule(TestCase):
    def test_number_of_states(self):
        """Number of states plus DC"""
        self.assertEqual(len(us_states), 51)
