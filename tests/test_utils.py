import sys
import os
import unittest
import datetime as dt

sys.path.append(os.path.dirname(os.getcwd()) + "/bibot")

import utils as u

class TestStringMethods(unittest.TestCase):

    def test_date_to_timestamp_millis(self):
        self.assertEqual(u.date_to_timestamp_millis("2022-12-01"), 1669852800000)
    

if __name__ == "__main__":
     unittest.main()