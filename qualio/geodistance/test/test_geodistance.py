#!/usr/bin/env python

__author__ = 'shay delaney'
__date__ = '22/04/2016'

"""
test_geodistance.py:

A test suite to run against the geodistance.py program

Assumptions
-----------
1.  The reading and loading of the data is not tested as I didn't deem it necessary to
    test the urlopen function in the urllib.request module. I think that is beyond the scope
    of these tests.
    Instead I read in a small snapshot, taken from the url, of sample data from a local file
    called cities-sample.json. This will serve as our test data.

2.  I am also assuming that the url provided contains valid json data. I have included tests
    for checking that data is in valid format.

3.  I use the Pycharm IDE to run these tests but if you want to run testsuite from command line,
    I use nosetests package. They can be run from inside the qualio\geodistance folder
    when you unzip the package.

"""

import os, sys, unittest, json
# setting geodistance folder onto classpath so tests will run from command line
sys.path.append("geodistance")

from geodistance import GreatCircleDistance


class GreatCircleTestCase(unittest.TestCase):
    """
    A class which will be our TestCase class for testing the GreatCircleDistance class
    in geodistance.py
    """

    def setUp(self):
        self.gcd = GreatCircleDistance()
        script_path = os.path.abspath(__file__)             # current path of this file
        self.resources_dir = os.path.split(script_path)[0]  # current path of this script

    def test_calculate_distance_valid(self):
        """ Calculates a valid distance between Aberdeen and Dublin """

        lat = 57.15     # Aberdeen latitude
        lon = -2.1      # Aberdeen longitude
        distance = self.gcd.calculate_distance(lat, lon)
        self.assertEqual(499.716888643048, distance)


    def test_calculate_distance_incorrect(self):
        """ Calculates an incorrect distance between Minneapolis and Dublin """

        lat = 44.967     # Minneapolis latitude
        lon = -93.25     # Minneapolis longitude
        distance = self.gcd.calculate_distance(lat, lon)

        # Correct distance = 5994.207918161822
        self.assertLessEqual(5994, distance)
        self.assertNotEquals(6000, distance)
        self.assertNotEquals(5994.30, distance)
        self.assertGreater(5995,distance)


    def test_calculate_distance_invalid_with_zero_values(self):
        """ Calculates a set of zero coordinates """

        lat = 0.0
        lon = 0.0
        distance = self.gcd.calculate_distance(lat, lon)

        # Correct distance = 5958.657075587726
        self.assertNotEquals(5995,distance)


    def test_process_json_data(self):
        """
        Tests the process_json_data against sample data. This will also make a call to
        the calculate_distance function
        """

        # Open sample data file from resources directory
        # Exact path can change depending on where we run it from, hence the path construction
        datafile = os.path.join(self.resources_dir, 'resources/cities-sample.json')

        with open(datafile) as json_data:
            self.json_records = json.load(json_data)
            json_data.close()

        city_list = self.gcd.process_json_data(self.json_records)

        # Correct result = 3 (Leeds, Birmingham, Aberdeen)
        self.assertEquals(3, int(len(city_list)))
        self.assertNotEquals(4, int(len(city_list)))


    def test_initialise_data_bad_data(self):
        """
        Tests the process_initialise_data against bad sample data.
        """

        # Open sample data file from resources directory
        # Exact path can change depending on where we run it from, hence the path construction
        datafile = os.path.join(self.resources_dir, 'resources/cities-invalid.json')

        try:
            filehandler = open(datafile)
            location_data = filehandler.read()
            self.json_records = self.gcd.initialise_data(location_data)
        finally:
            filehandler.close()

        # Correct result = "Data Initialisation Failure"
        self.assertEquals("Data Initialisation Failure", self.json_records)
        self.assertNotEquals(44, len(self.json_records))


    def test_initialise_data_clean_data(self):
        """
        Tests the process_initialise_data against clean sample data.
        """

        # Open sample data file from resources directory
        # Exact path can change depending on where we run it from, hence the path construction
        datafile = os.path.join(self.resources_dir, 'resources/cities-sample.json')
        
        try:
            filehandler = open(datafile)
            location_data = filehandler.read()
            self.json_records = self.gcd.initialise_data(location_data)
        finally:
            filehandler.close()

        # Correct result = 44 records in dict
        self.assertEquals(44, len(self.json_records))
        self.assertNotEquals("Data Initialisation Failure", self.json_records)


if __name__ == '__main__':
    unittest.main()
