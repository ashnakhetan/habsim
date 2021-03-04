import datetime
from . import util
import math
import random
import bisect
import numpy as np

class Trajectory(list):
    # superclass of list
    def __init__(self, data=list()):
        super().__init__(data)
        self.data = data

    def duration(self):
        '''
        Returns duration in hours, assuming the first field of each tuple is a UNIX timestamp.
        '''
        # these are datetime objects, call .seconds()
        # rolls over with days
        return (self.data[len(self.data) - 1].time - self.data[0].time).total_seconds() / 3600

    def length(self):
        '''
        Distance travelled by trajectory in km.
        '''
        res = 0
        for i, j in zip(self[:-1], self[1:]):
            res += i.location.distance(j.location)
        return res

    def interpolate(self, time):
        # find where it is between locations
        # return location and altitude
        pass

class Record:
    def __init__(self, time, location, alt, vrate, airvector, windvector):
        self.time = time
        self.location = location
        self.alt = alt
        # naming
        self.ascent_rate = vrate
        self.air_vector = airvector
        self.wind_vector = windvector

class Location(tuple): # subclass of tuple, override __iter__
    # unpack lat and lon as two arguments when passed into a function, *
    EARTH_RADIUS = 6371.0

    # super class
    # dont store instance variables
    # define getter functions
    def __new__(self, lat, lon):
        print("new")
        return tuple.__new__(Location, (lat, lon))

    # def __init__(self, lat, lon):
    #     print("constructor")
    #     self.lat = lat
    #     self.lon = lon

    def getLon(self):
        return self[1]

    def getLat(self):
        return self[0]

    def distance(self, other):
        # change to indices
        return self.haversine(self[0], self.lon, other.lat, other.lon)

    def haversine(self, lat1, lon1, lat2, lon2):
        '''
        Returns great circle distance between two points.
        '''
        # what will happen if distance called between invalid point (lat out of bounds)
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2-lat1
        dlon = lon2-lon1

        a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return EARTH_RADIUS * c

class ElevationFile:
    # res may not be 120
    resolution = 120 ## points per degree

    def __init__(self, path): # store
        self.data = np.load(path, 'r')

    def elev(self, lat, lon): # return elevation
        x = int(round((lon + 180) * resolution))
        y = int(round((90 - lat) * resolution)) - 1
        return max(0, data[y, x])