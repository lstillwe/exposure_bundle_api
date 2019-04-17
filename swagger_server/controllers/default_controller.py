import connexion
import six

from swagger_server.models.exposures_bundle import ExposuresBundle  # noqa: E501
from swagger_server import util


def get_exposures(coords_file, start_date=None, end_date=None):  # noqa: E501
    """provided with list of lat,lons in a file (1 pair on each line) will return a bundle of exposure types (CMAQ, roadway, &amp; socio-economic)

    By passing in the appropriate options, you can get a bundle of exposure types (CMAQ, roadway, &amp; socio-economic)  # noqa: E501

    :param coords_file: input file with list of lat,lon coordinates (1 pair per line; decimal format - WGS84 assumed)
    :type coords_file: werkzeug.datastructures.FileStorage
    :param start_date: start date of range (ex: 2010-01-01) - if not provided, no CMAQ data will be returned
    :type start_date: str
    :param end_date: end date of range (ex: 2010-01-02) - if not provided, no CMAQ data will be returned
    :type end_date: str

    :rtype: ExposuresBundle
    """
    print("Lisa - I got into default_controller:get_exposures")
    if (start_date):
        start_date = util.deserialize_date(start_date)
    if (end_date):
        end_date = util.deserialize_date(end_date)

    from swagger_server.exposures.exposures import Exposures
    exp = Exposures()
    kwargs = locals()
    data = exp.get_values(**kwargs)

    return data
