# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.exposures_bundle import ExposuresBundle  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_exposures(self):
        """Test case for get_exposures

        provided with list of lat,lons in a file (1 pair on each line) will return a bundle of exposure types (CMAQ, roadway, & socio-economic)
        """
        query_string = [('start_date', '2013-10-20'),
                        ('end_date', '2013-10-20')]
        data = dict(coords_file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/lstillwell/exposure-bundle-api/1.0.0/exposures',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
