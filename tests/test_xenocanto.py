import pytest
import requests
from unittest import mock
from requests import HTTPError
from pyxctools.xenocanto import XenoCanto


class TestXenoCanto:

    # Create common XenoCanto class to be shared by all tests.
    @pytest.fixture(name="xc")
    def create_xc(self):
        xc = XenoCanto()
        return xc

    def _mock_response(self,
                       status_code: int = requests.codes.ok,
                       json_data: dict = None,
                       raise_for_status: Exception = None) -> mock.Mock:
        """
        Helper method to generate a mock response.

        :param status_code: Status code to give the mock response.
        :param json_data: JSON data to give the mock response.
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
            mock_resp.json = mock.Mock(return_value=json_data)

        return mock_resp

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_get_response(self, mock_get, xc):
        QUERY_STRING = "common snipe"

        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp

        # If the request is unsuccessful, or json decoding fails, the query method will raise an exception.
        r = xc._get(QUERY_STRING)

        assert r is not None
        assert mock_resp.raise_for_status.called

    @mock.patch("pyxctools.xenocanto.requests.get")
    def test_failed_response(self, mock_get, xc):
        QUERY_STRING = "common snipe"

        mock_resp = self._mock_response(status_code=requests.codes.internal_server_error,
                                        raise_for_status=HTTPError("xeno-canto is down."))
        mock_get.return_value = mock_resp

        # This response should raise a HTTPError as it returned an unsuccessful status code (500).
        with pytest.raises(HTTPError):
            xc._get(QUERY_STRING)
