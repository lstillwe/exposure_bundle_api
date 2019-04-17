import sys
from datetime import datetime, timedelta
from sqlalchemy import extract, func, cast
from geoalchemy2 import Geography
import pytz
from swagger_server.exposures.exposure_values_abstract import EnvExposureValue


class SocioEconExposures(EnvExposureValue):

    def get_exposure_values(self, coords):

        # retrieve query result for each lat,lon pair and add to data object
        print(coords)

        # create data object
        data = {'socio_econ': []}

        for coord in coords:
            lat = coord['lat']
            lon = coord['lon']
            print(lat)
            print(lon)

            session = self.exp_module.Session() 

            # given this lat lon, find the census tract that contains it.
            query = session.query(self.exp_module.CensusBlockGrp.geoid). \
                                filter(func.ST_Contains(self.exp_module.CensusBlockGrp.geom,
                                        func.ST_GeomFromText("POINT(" + str(lon) + " " + str(lat) + ")", 4269)))
            result = session.execute(query)
            session.close()
            for query_return_values in result:
                geoid = query_return_values[0]
             
            print(geoid)

            # daily resolution of data - return only matched hours for date range
            session = self.exp_module.Session() 
            query = session.query(self.exp_module.SocioEconomicDatum.id,
                                  self.exp_module.SocioEconomicDatum.geoid,
                                  self.exp_module.SocioEconomicDatum.estresidentialdensity,
                                  self.exp_module.SocioEconomicDatum.estresidentialdensity_se,
                                  self.exp_module.SocioEconomicDatum.estresidentialdensity25plus,
                                  self.exp_module.SocioEconomicDatum.estresidentialdensity25plus_se,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynonhispwhite,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynonhispwhite_se,
                                  self.exp_module.SocioEconomicDatum.estprobabilityhighschoolmaxeducation,
                                  self.exp_module.SocioEconomicDatum.estprobabilityhighschoolmaxeducation_se,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynoauto,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynoauto_se,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynohealthins,
                                  self.exp_module.SocioEconomicDatum.estprobabilitynohealthins_se,
                                  self.exp_module.SocioEconomicDatum.estprobabilityesl,
                                  self.exp_module.SocioEconomicDatum.estprobabilityesl_se,
                                  self.exp_module.SocioEconomicDatum.esthouseholdincome,
                                  self.exp_module.SocioEconomicDatum.esthouseholdincome_se). \
                                      filter(self.exp_module.SocioEconomicDatum.geoid.like("%" + geoid))

	
            for query_return_values in query:
                data['socio_econ'].append({'latitude': lat,
                                           'longitude': lon,
                                           'geoid': query_return_values[1],
                                           'EstTotalPop': int(query_return_values[2]),
                                           'EstTotalPop_SE': float(query_return_values[3]),
                                           'EstTotalPop25Plus': int(query_return_values[4]),
                                           'EstTotalPop25Plus_SE': float(query_return_values[5]),
                                           'EstPropPersonsNonHispWhite': float(query_return_values[6]),
                                           'EstPropPersonsNonHispWhite_SE': float(query_return_values[7]),
                                           'EstPropPersons25PlusHighSchoolMax': float(query_return_values[8]),
                                           'EstPropPersons25PlusHighSchoolMax_SE': float(query_return_values[9]),
                                           'EstPropHouseholdsNoAuto': float(query_return_values[10]),
                                           'EstPropHouseholdsNoAuto_SE': float(query_return_values[11]),
                                           'EstPropPersonsNoHealthIns': float(query_return_values[12]),
                                           'EstPropPersonsNoHealthIns_SE': float(query_return_values[13]),
                                           'EstPropPersons5PlusNoEnglish': float(query_return_values[14]),
                                           'EstPropPersons5PlusNoEnglish_SE': float(query_return_values[15]),
                                           'MedianHouseholdIncome': query_return_values[16],
                                           'MedianHouseholdIncome_SE': query_return_values[17]})

            session.close()

        return data
