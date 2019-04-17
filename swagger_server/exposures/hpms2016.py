import sys
from configparser import ConfigParser
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography

#from swagger_server.controllers import Session
from flask import jsonify
#from swagger_server.models.models import TlRoad
#from swagger_server.models.models import Hpms2016MajorRoad
from enum import Enum
from swagger_server.exposures.exposure_values_abstract import EnvExposureValue



rdTypeDict = {'01':'Off-Network','02':'Rural Restricted Access','03':'Rural Unrestricted Access',
        '04':'Urban Restricted Access','05':'Urban Unrestricted Access'}

class Hpms2016Proximity(EnvExposureValue):


    def get_exposure_values(self, coords):
        # latitude, logitude, limit_distance=500


        #limit = kwargs.get('limit_distance')
        limit = 500

        # create data object
        data = {'proximity': []}

        for coord in coords:
            lat = coord['lat']
            lon = coord['lon']

            session = self.exp_module.Session()
        
            query = "select route_id, roadtype, aadt, speed, through_lanes, st_distancesphere(geom, ST_GeomFromText('POINT(" + str(lon) + " " + str(lat) + ")',4269)) as distance from hpms2016_major_roads  where st_dwithin(geom::geography, ST_SetSRID(ST_MakePoint(" + str(lon) + ", " + str(lat) + "),4269)::geography," + str(limit) + ") order by distance, roadtype DESC"

            result = session.execute(query)

            for query_return_values in result:

                data['proximity'].append({'route_id': query_return_values[0],
                             'roadtype': rdTypeDict[query_return_values[1]],
                             'latitude': lat,
                             'longitude': lon,
                             'distance': query_return_values[5],
                             'aadt':query_return_values[2],
                             'speed':query_return_values[3],
                             'through_lanes': query_return_values[4]})
                break

            session.close()

        return data
