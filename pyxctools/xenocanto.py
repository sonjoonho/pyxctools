import csv
import os
import logging
from pathlib import Path

import requests

from pyxctools.constants import XC_BASE_URL


class XenoCanto:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

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
        """
        Returns JSON from the API call with the given search terms.

        :param search_terms: The terms to query xeno-canto for.
        :return: A dictionary that represents the JSON returned by the xeno-canto API.
        """
        r = self._get(search_terms)
        query_json = r.json()
        return query_json

    def download_files(self, search_terms: str, dir: str = "sounds"):
        # Raises a FileNotFoundError if the directory does not exist.
        path = Path(dir).resolve()

        if not os.path.exists(path):
            self.logger.debug(f"Created new directory at {path}.")
            os.makedirs(path)

        file_data = self.query(search_terms)

        # Download recording and write metadata
        for recording in file_data["recordings"]:
            with requests.get(f"http:{recording['file']}", allow_redirects=True, stream=True) as r:
                # Note that xeno-canto only supports mp3s.
                with open(f"{path / recording['id']}.mp3", "wb") as f:
                    f.write(r.content)
            self.logger.info(f"Downloaded{path / recording['id']}.")

        keys = file_data["recordings"][0].keys()

        # Save metadata
        with open(path / "metadata.csv", "w") as f:
            w = csv.DictWriter(f, keys)
            w.writeheader()
            w.writerows(file_data["recordings"])
        self.logger.info("Download metadata.")
