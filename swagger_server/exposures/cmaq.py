import sys
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography

import pytz
#from swagger_server.controllers import Session
from flask import jsonify
#from swagger_server.models.models import ExposureDatum, ExposureList, CensusTract
from swagger_server.exposures.exposure_values_abstract import EnvExposureValue
from enum import Enum


class CmaqExposures(EnvExposureValue):

    def get_exposure_values(self, coords, start_time, end_time):
 
        print(str(start_time))
        print(str(end_time))

         # 'UTC', 'US/Central', 'US/Eastern','US/Mountain', 'US/Pacific'
        tzone_dict = {'utc': 'UTC',
                      'eastern': 'US/Eastern',
                      'central': 'US/Central',
                      'mountain': 'US/Mountain',
                      'pacific': 'US/Pacific'}

        # create data object
        data = {}
        vals = {'values': []}
        data['cmaq'] = vals
        #data = {'cmaq': []}
        print(data)

        # set UTC offset as time zone parameter for query
        dt = datetime.now()
        utc_offset = int(str(pytz.timezone(tzone_dict.get("utc")).localize(dt)
                             - pytz.utc.localize(dt)).split(':')[0])

        # retrieve query result for each lat,lon pair and add to data object
        var_set = {'ozone_daily_8hour_maximum', 'pm25_daily_average'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################

        for coord in coords:
            lat = coord['lat']
            lon = coord['lon']

            for var in var_set:
                # determine exposure type to query
                cmaq_output = []

                exposure = var

                session = self.exp_module.Session()

                # given this lat lon, find the census tract that contains it.
                query = session.query(self.exp_module.CensusTract.geoid). \
                                filter(func.ST_Contains(self.exp_module.CensusTract.geom, func.ST_GeomFromText("POINT(" + str(lon) + " " + str(lat) + ")", 4269)))
                result = session.execute(query)
                for query_return_values in result:
                    geoid = query_return_values[0]
                session.close()


                session = self.exp_module.Session()
                # daily resolution of data - return only matched hours for date range
                query = session.query(self.exp_module.ExposureDatum.id,
                                      self.exp_module.ExposureDatum.date,
                                      getattr(self.exp_module.ExposureDatum, exposure)). \
                                      filter(self.exp_module.ExposureDatum.date >= start_time + timedelta(hours=utc_offset)). \
                                      filter(self.exp_module.ExposureDatum.date <= end_time + timedelta(hours=utc_offset)). \
                                      filter(self.exp_module.ExposureDatum.fips == geoid). \
                                      filter(extract('hour', self.exp_module.ExposureDatum.date) == utc_offset)

                # add query output to data object in JSON structured format
                                      #filter(extract('hour', self.exp_module.ExposureDatum.date) == utc_offset)
                for query_return_values in query:
                        cmaq_output.append({'date': query_return_values[1].strftime("%Y-%m-%d"),
                                            'value': float(query_return_values[2])})
                session.close()
                data['cmaq']['values'].append({'variable': var,
                                       'latitude': lat,
                                       'longitude': lon,
                                       'cmaq_output': cmaq_output})

        return data
