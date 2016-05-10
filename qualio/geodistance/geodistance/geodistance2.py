#!/usr/bin/env python

__author__ = 'shay delaney'
__date__ = '22/04/2016'

""" 
geodistance2.py:

A python program to find any city within 500km of Dublin.

This program will read a full list of cities from a file (url) and output the names of cities in
a 500 km radius from Dublin, sorted by name (ascending).

To calculate the distance between two coordinates, Great-circle distance is used.
Reference : https://en.wikipedia.org/wiki/Great-circle_distance
Haversine Formula

"""

import json, urllib.request
import math

# Constants

# URL to read location data from
JSON_URL = "https://gist.githubusercontent.com/mwtorkowski/16ca26a0c072ef743734/raw/2aa20e8de9f2292d58a4856602c1f0634d8611a7/cities.json"

DUBLIN_LOC = (53.333, -6.267)   # GPS coordinates of Dublin as a tuple
KMS_RADIUS = 500                # 500Km radius of Dublin
EARTH_RADIUS = 6371             # Earths radius in kilometers


class Location:
    """
    An object that represents a location read in from our data file.
    It contains latitude and longitude coordinates of a location, the city name, and a
    value to store is proximity from Dublin
    """

    def __init__(self, city, lat, lon):
        """ Constructor for Location class """
        self.lat = lat
        self.lon = lon
        self.distance = 0
        self.city = city

    def __repr__(self):
        return str(self.city)


class GreatCircleDistance:
    """
    The main class which handles loading and processing of data, as well as a function to calculate
    the Great-circle distance formula (Haversine)
    """
    def __init__(self):
        # Initialise Dublin lat and lon points in the class, store as radians
        self.lat2 = math.radians(DUBLIN_LOC[0])
        self.lon2 = math.radians(DUBLIN_LOC[1])

    def initialise_data(self, jsondata):
        """
        Decodes the json data
        Returns a dictionary of json records
        """

        try:
           json_location_records = json.loads(jsondata)
           return json_location_records

        except ValueError:
            print('Failed to decode JSON data in input')
            return "Data Initialisation Failure"


    def calculate_distance(self, lat, lon):
        """ Calculates distance between two poinrs.
                Point 1. Passed in latitude and longitude coordinates
                Point 2. Dublin's latitude and longitude coordinates
            Returns distance in kilometers
        """

        # convert degrees to radians
        lat1 = math.radians(lat)
        lon1 = math.radians(lon)

        # Great-circle distance - Haversine
        lat_radians = self.lat2 - lat1
        lon_radians = self.lon2 - lon1

        a = (math.sin(lat_radians / 2) ** 2) + (math.cos(lat1) * math.cos(self.lat2)) * (math.sin(lon_radians / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        # Multiply by radius of Earth in Km's to get distance in Km's.
        d = EARTH_RADIUS * c

        return d


    def check_record(self, location):

        # construct a Location object from the record
        #c = Location( location['city'], location['lat'], location['lon'])

        # call function to calculate distance
        #distance = self.calculate_distance(c.lat, c.lon)

        #if distance <= KMS_RADIUS:
            #c.distance = distance       # set distance into Location object
            #return c    # add city to list of cities
        return location['city'] if self.calculate_distance(location['lat'], location['lon']) <= KMS_RADIUS else None


    def process_json_data(self, json_city_records):
        """
        Process a dict of json city records.
        Call function to calculate distance between two points.
        Return list of cities whose location is within 500km of Dublin.
        """
        list_of_cities = [record for record in json_city_records if self.check_record(json_city_records[record])]

        # sort list by city attribute
        list_of_cities.sort()

        return list_of_cities


def load_data():
    """
    Loads the locations json data in from the URL
    """
    try:
        location_data = urllib.request.urlopen(JSON_URL).read().decode('utf8')
        return location_data

    except urllib.error.URLError as e:
        print(e.reason)
        return None


if __name__ == '__main__':

    # read data in from url
    data = load_data()

    if data:
        # instantiate GreatCircleDistance class
        gcd = GreatCircleDistance()

        # call function to read in and load data
        json_data = gcd.initialise_data(data)

        if json_data:
            # get a list of cities within 500km of Dublin
            list_within_radius = gcd.process_json_data(json_data)

            print("List of cities in 500km radius from Dublin:")
            print("-------------------------------------------")

            # print list as separate args
            print(*list_within_radius, sep='\n')
            print("\nTotal: " + str(len(list_within_radius)))

        else:
            print("A problem occurred decoding the json data")

    else:
        print("A problem occurred reading the data file")