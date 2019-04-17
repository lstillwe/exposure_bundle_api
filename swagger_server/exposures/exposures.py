# do all the work of rading lat lon file and calling other exposure services here to build big response.
# still have to decide how to return response - i.e. via email??

import sys
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography

import pytz
#from swagger_server.controllers import DB
from flask import jsonify
#from swagger_server.models.cmaq.model import ExposureDatum, ExposureList, CensusTract
#from swagger_server.models.proximity.model import Hpms2016MajorRoad
#from swagger_server.models.social.model import SocioEconomicDatum, CensusBlockGrp
from swagger_server.models.databases import Databases
from swagger_server.exposures.socio_econ import SocioEconExposures
from swagger_server.exposures.hpms2016 import Hpms2016Proximity
from swagger_server.exposures.cmaq import CmaqExposures
from swagger_server.models import settings

parser = ConfigParser()
parser.read('swagger_server/models/cmaq/connexion.ini')
sys.path.append(parser.get('sys-path', 'exposures'))
sys.path.append(parser.get('sys-path', 'controllers'))
from enum import Enum


class MeasurementType(Enum):
    # lat: 0 to +/- 90, lon: 0 to +/- 180 as lat,lon

    LATITUDE = '^[+-]?(([1-8]?[0-9])(\.[0-9]+)?|90(\.0+)?)$'
    LONGITUDE = '^[+-]?((([1-9]?[0-9]|1[0-7][0-9])(\.[0-9]+)?)|180(\.0+)?)$'

    def isValid(self, measurement):
        import re
        if re.match(self.value, str(measurement)) is None:
            return False
        else:
            return True

class Exposures(object):

    def is_valid_lat_lon(self, **kwargs):
        # lat: 0 to +/- 90, lon: 0 to +/- 180 as lat,lon
        if not MeasurementType.LATITUDE.isValid(kwargs.get('latitude')):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: latitude'})
        if not MeasurementType.LONGITUDE.isValid(kwargs.get('longitude')):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: longitude'})

        return True, ''

    def is_valid_date_range(self, **kwargs):
        #session = Session()
        var_set = {'o3', 'pm25'} ################ TODO: CHANGE THIS TO GET FULL SET FROM DB #################
        for var in var_set:
            min_date = session.query(ExposureList.utc_min_date).filter(
                ExposureList.variable == var).one()
            max_date = session.query(ExposureList.utc_max_date).filter(
                ExposureList.variable == var).one()
            session.close()
            if min_date[0] > kwargs.get('end_date'):
                return False
            elif max_date[0] < kwargs.get('start_date'):
                return False
            elif kwargs.get('start_date') > kwargs.get('end_date'):
                return False

        return True

    def validate_parameters(self, **kwargs):
        lat_lon_valid, msg = self.is_valid_lat_lon(**kwargs)

        if not self.is_valid_date_range(**kwargs):
            return False, ('Invalid parameter', 400, {'x-error': 'Invalid parameter: start_date, end_date'})
        elif not lat_lon_valid:
            return False, msg
        else:
            return True, ''

    def get_values(self, **kwargs):
        # latitude, longitude
        print("Lisa - I am now in get_values")

        # validate input from user
        #is_valid, message = self.validate_parameters(**kwargs)
        #if not is_valid:
            #return message

        # create data object
        data = {}
        #data['values'] = []

        # retrieve query result for each lat,lon pair and add to data object
        coords = []
        ifile = kwargs.get('coords_file')
        if ifile:
            for coord_set in ifile:
                coord_set = str(coord_set.decode("utf-8")).rstrip()
                lat, lon = coord_set.split(',') 
                lat = lat.lstrip().rstrip()
                lon = lon.lstrip().rstrip()
                coords.append({'lat': lat, 'lon': lon})
        else:
            # lat, lon required to continue =>>> return an error here
            placeholder = True

        #for database in settings.INSTALLED_DATABASES:
        socio_exp = SocioEconExposures("social")
        socio_exp_data = socio_exp.get_exposure_values(coords)
        data.update(socio_exp_data)
        roadway_exp = Hpms2016Proximity("proximity")
        roadway_exp_data = roadway_exp.get_exposure_values(coords)
        data.update(roadway_exp_data)
        cmaq_exp = CmaqExposures("cmaq")
        cmaq_exp_data = cmaq_exp.get_exposure_values(coords, kwargs.get('start_date'), kwargs.get('end_date'))
        data.update(cmaq_exp_data)
 

        return jsonify(data)
