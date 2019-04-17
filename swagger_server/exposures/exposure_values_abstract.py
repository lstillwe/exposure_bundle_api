# abstract class for use in writing classes to support extraction of environmental
# exposure values

from abc import ABCMeta, abstractmethod, abstractproperty
from swagger_server.models.databases import Databases 


class EnvExposureValue:

    __metaclass__ = ABCMeta

    def __init__(self, exposure_type):

        db = Databases()
        module_path = "swagger_server.models." + exposure_type
        self.exp_module = __import__(module_path, fromlist=exposure_type)


    @abstractmethod
    def get_exposure_values(self, coords, start_time, end_time):

        # must supply this method
        # retrieve exposure values and return in array of dict
        # kwargs are already validated

        # if retrieveing data from DB, add infrastructure for new model to models/ 
        # using example of existing exposure types

        pass

