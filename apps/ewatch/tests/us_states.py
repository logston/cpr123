from django.test import TestCase

from libs.ref.us_states import us_states

class TestUSStatesModule(TestCase):
    def test_number_of_states(self):
        """Number of states plus DC"""
        self.assertEqual(len(us_states), 51)

    def test_len_of_states_appriviation(self):
        """Length of state appriviation should always be 2"""
        for state in us_states:
            self.assertEqual(len(state[0]), 2)
