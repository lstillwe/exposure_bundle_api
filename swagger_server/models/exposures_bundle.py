# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.exposures_bundle_cmaq import ExposuresBundleCmaq  # noqa: F401,E501
from swagger_server.models.exposures_bundle_roadway import ExposuresBundleRoadway  # noqa: F401,E501
from swagger_server.models.exposures_bundle_socioecon import ExposuresBundleSocioecon  # noqa: F401,E501
from swagger_server import util


class ExposuresBundle(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, latitude1: str=None, longitude1: str=None, cmaq: ExposuresBundleCmaq=None, roadway: ExposuresBundleRoadway=None, socio_econ: ExposuresBundleSocioecon=None):  # noqa: E501
        """ExposuresBundle - a model defined in Swagger

        :param latitude1: The latitude1 of this ExposuresBundle.  # noqa: E501
        :type latitude1: str
        :param longitude1: The longitude1 of this ExposuresBundle.  # noqa: E501
        :type longitude1: str
        :param cmaq: The cmaq of this ExposuresBundle.  # noqa: E501
        :type cmaq: ExposuresBundleCmaq
        :param roadway: The roadway of this ExposuresBundle.  # noqa: E501
        :type roadway: ExposuresBundleRoadway
        :param socio_econ: The socio_econ of this ExposuresBundle.  # noqa: E501
        :type socio_econ: ExposuresBundleSocioecon
        """
        self.swagger_types = {
            'latitude1': str,
            'longitude1': str,
            'cmaq': ExposuresBundleCmaq,
            'roadway': ExposuresBundleRoadway,
            'socio_econ': ExposuresBundleSocioecon
        }

        self.attribute_map = {
            'latitude1': 'latitude1',
            'longitude1': 'longitude1',
            'cmaq': 'cmaq',
            'roadway': 'roadway',
            'socio_econ': 'socio-econ'
        }

        self._latitude1 = latitude1
        self._longitude1 = longitude1
        self._cmaq = cmaq
        self._roadway = roadway
        self._socio_econ = socio_econ

    @classmethod
    def from_dict(cls, dikt) -> 'ExposuresBundle':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ExposuresBundle of this ExposuresBundle.  # noqa: E501
        :rtype: ExposuresBundle
        """
        return util.deserialize_model(dikt, cls)

    @property
    def latitude1(self) -> str:
        """Gets the latitude1 of this ExposuresBundle.


        :return: The latitude1 of this ExposuresBundle.
        :rtype: str
        """
        return self._latitude1

    @latitude1.setter
    def latitude1(self, latitude1: str):
        """Sets the latitude1 of this ExposuresBundle.


        :param latitude1: The latitude1 of this ExposuresBundle.
        :type latitude1: str
        """

        self._latitude1 = latitude1

    @property
    def longitude1(self) -> str:
        """Gets the longitude1 of this ExposuresBundle.


        :return: The longitude1 of this ExposuresBundle.
        :rtype: str
        """
        return self._longitude1

    @longitude1.setter
    def longitude1(self, longitude1: str):
        """Sets the longitude1 of this ExposuresBundle.


        :param longitude1: The longitude1 of this ExposuresBundle.
        :type longitude1: str
        """

        self._longitude1 = longitude1

    @property
    def cmaq(self) -> ExposuresBundleCmaq:
        """Gets the cmaq of this ExposuresBundle.


        :return: The cmaq of this ExposuresBundle.
        :rtype: ExposuresBundleCmaq
        """
        return self._cmaq

    @cmaq.setter
    def cmaq(self, cmaq: ExposuresBundleCmaq):
        """Sets the cmaq of this ExposuresBundle.


        :param cmaq: The cmaq of this ExposuresBundle.
        :type cmaq: ExposuresBundleCmaq
        """

        self._cmaq = cmaq

    @property
    def roadway(self) -> ExposuresBundleRoadway:
        """Gets the roadway of this ExposuresBundle.


        :return: The roadway of this ExposuresBundle.
        :rtype: ExposuresBundleRoadway
        """
        return self._roadway

    @roadway.setter
    def roadway(self, roadway: ExposuresBundleRoadway):
        """Sets the roadway of this ExposuresBundle.


        :param roadway: The roadway of this ExposuresBundle.
        :type roadway: ExposuresBundleRoadway
        """

        self._roadway = roadway

    @property
    def socio_econ(self) -> ExposuresBundleSocioecon:
        """Gets the socio_econ of this ExposuresBundle.


        :return: The socio_econ of this ExposuresBundle.
        :rtype: ExposuresBundleSocioecon
        """
        return self._socio_econ

    @socio_econ.setter
    def socio_econ(self, socio_econ: ExposuresBundleSocioecon):
        """Sets the socio_econ of this ExposuresBundle.


        :param socio_econ: The socio_econ of this ExposuresBundle.
        :type socio_econ: ExposuresBundleSocioecon
        """

        self._socio_econ = socio_econ
