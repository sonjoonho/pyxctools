import pytest
import requests
import json
import logging
from unittest import mock
from requests import HTTPError
from pyxctools.xenocanto import XenoCanto


class TestXenoCanto:

    # Create common XenoCanto class to be shared by all tests.
    @pytest.fixture(name="xc")
    def create_xc(self):
        xc = XenoCanto()
        xc.logger.setLevel(logging.DEBUG)
        return xc

    def _mock_response(self,
                       status_code: int = requests.codes.ok,
                       json_data: str = None,
                       raise_for_status: Exception = None) -> mock.Mock:
        """
        Helper method to generate a mock response.

        :param status_code: Status code to give the mock response.
        :param json_data: JSON encoded data to give the mock response.
        :param raise_for_status: The side effect that raise_for_status will call. Usually HTTPException.
        :return: The mock response.
        """
        # Mock our response object.
        mock_resp = mock.Mock()

        # Mock raise_for_status with optional error.
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status_code

        if json_data:
            mock_resp.json = mock.Mock(return_value=json.loads(json_data))

        return mock_resp

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_query(self, mock_get, xc):
        QUERY_STRING = "Myrmecocichla monticola"
        EXAMPLE_JSON = {'numRecordings': '13', 'numSpecies': '1', 'page': 1, 'numPages': 1, 'recordings': [
            {'id': '388321', 'gen': 'Myrmecocichla', 'sp': 'monticola', 'ssp': '', 'en': 'Mountain Wheatear',
             'rec': 'Faansie Peacock', 'cnt': 'South Africa', 'loc': 'Kagga Kamma PNR, Western Cape', 'lat': '-32.7431',
             'lng': '19.5567', 'type': 'call, song', 'file': '//www.xeno-canto.org/388321/download',
             'lic': '//creativecommons.org/licenses/by-nc-sa/4.0/', 'url': 'https://www.xeno-canto.org/388321',
             'q': 'A', 'time': '08:00', 'date': '2017-09-26'},
            {'id': '382995', 'gen': 'Myrmecocichla', 'sp': 'monticola', 'ssp': '', 'en': 'Mountain Wheatear',
             'rec': 'Faansie Peacock', 'cnt': 'South Africa', 'loc': 'Clanwilliam, Cederberg, Western Cape',
             'lat': '-32.1414', 'lng': '19.0194', 'type': 'call, song', 'file': '//www.xeno-canto.org/382995/download',
             'lic': '//creativecommons.org/licenses/by-nc-sa/4.0/', 'url': 'https://www.xeno-canto.org/382995',
             'q': 'A', 'time': '06:30', 'date': '2017-07-01'},
            {'id': '382994', 'gen': 'Myrmecocichla', 'sp': 'monticola', 'ssp': '', 'en': 'Mountain Wheatear',
             'rec': 'Faansie Peacock', 'cnt': 'South Africa', 'loc': 'Clanwilliam, Cederberg, Western Cape',
             'lat': '-32.1414', 'lng': '19.0194', 'type': 'song', 'file': '//www.xeno-canto.org/382994/download',
             'lic': '//creativecommons.org/licenses/by-nc-sa/4.0/', 'url': 'https://www.xeno-canto.org/382994',
             'q': 'A', 'time': '06:00', 'date': '2017-07-01'}]}

        mock_resp = self._mock_response(json_data=json.dumps(EXAMPLE_JSON))
        mock_get.return_value = mock_resp

        query_return = xc.query(QUERY_STRING)

        assert query_return == EXAMPLE_JSON

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_failed_response(self, mock_get, xc):
        QUERY_STRING = "common snipe"

        mock_resp = self._mock_response(status_code=requests.codes.internal_server_error,
                                        raise_for_status=HTTPError("xeno-canto is down."))
        mock_get.return_value = mock_resp

        # This response should raise a HTTPError as it returned an unsuccessful status code (500).
        with pytest.raises(HTTPError):
            xc.query(QUERY_STRING)

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_advanced_query_1(self, mock_get, xc):

        EXAMPLE_JSON = {'numRecordings': '3', 'numSpecies': '1', 'page': 1, 'numPages': 1, 'recordings': [
            {'id': '228435', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228435/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228435',
             'q': 'B', 'time': '05:45', 'date': '2005-07-31'},
            {'id': '228434', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228434/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228434',
             'q': 'B', 'time': '05:45', 'date': '2005-07-30'},
            {'id': '228433', 'gen': 'Chordeiles', 'sp': 'nacunda', 'ssp': '', 'en': 'Nacunda Nighthawk',
             'rec': 'Peter Boesman', 'cnt': 'Brazil', 'loc': 'Pantanal, Pixaim area, Mato Grosso',
             'lat': '-16.6666666667',
             'lng': '-56.8333333333', 'type': 'song', 'file': '//www.xeno-canto.org/228433/download',
             'lic': '//creativecommons.org/licenses/by-nc-nd/4.0/', 'url': 'https://www.xeno-canto.org/228433',
             'q': 'C', 'time': '05:45', 'date': '2005-07-30'}]}

        mock_resp = self._mock_response(json_data=json.dumps(EXAMPLE_JSON))
        mock_get.return_value = mock_resp

        query_return = xc.query(country="brazil",
                                recordist="peter",
                                genus="Chordeiles",
                                latitude=-16.33666,
                                longitude=-56.553,
                                location="Pantanal, Pixaim area, Mato Grosso")

        assert query_return == EXAMPLE_JSON

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_empty_query(self, mock_get, xc):
        EXAMPLE_JSON = {"numRecordings": "0",
                        "numSpecies": "0",
                        "page": 1,
                        "numPages": 1,
                        "recordings": []}

        mock_resp = self._mock_response(json_data=json.dumps(EXAMPLE_JSON))
        mock_get.return_value = mock_resp
        with pytest.raises(Warning):
            xc.query(search_terms="foobar")

    def test_download(self, xc):
        xc.download_files(search_terms="Myrmecocichla monticola", dir="sounds")

        # TODO assert all files are correctly downloaded.
