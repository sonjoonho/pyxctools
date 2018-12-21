import requests

from pyxctools.constants import XC_BASE_URL


class XenoCanto:

    def __init__(self) -> None:
        pass

    def _get(self, search_terms: str) -> requests.Response:
        """
        Retrieves a HTTP response from the xeno-canto API.

        TODO Implement caching of requests.
        TODO Implement advanced query options.

        :param search_terms: The terms to query xeno-canto for.
        :return: The response.
        """
        r = requests.get(XC_BASE_URL, params={"query": search_terms})
        r.raise_for_status()

        return r

    def query(self, search_terms: str) -> dict:
        r = self._get(search_terms)
        query_json = r.json()
        return query_json
