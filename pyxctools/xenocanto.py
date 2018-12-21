import csv
import os
import logging
from pathlib import Path

import requests

from pyxctools.constants import XC_BASE_URL


class XenoCanto:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def query(self,
              query: str,
              genus: str = None,
              recordist: str = None,
              country: str = None,
              location: str = None,
              remarks: str = None,
              latitude: str = None,
              longitude: str = None,
              box: str = None,
              background_species: str = None,
              type: str = None,
              catalogue_number: str = None,
              license: str = None,
              quality: str = None,
              area: str = None,
              since: str = None,
              year: str = None,
              month: str = None) -> dict:

        """
        Returns JSON from the API call with the given search terms.

        For details of each parameter, see https://www.xeno-canto.org/help/search.

        TODO Implement caching of requests.

        :return: A dictionary that represents the JSON returned by the xeno-canto API.
        """
        payload = {"query": query,
                   "gen": genus,
                   "rec": recordist,
                   "cnt": country,
                   "loc": location,
                   "rmk": remarks,
                   "lat": latitude,
                   "lon": longitude,
                   "box": box,
                   "also": background_species,
                   "type": type,
                   "nr": catalogue_number,
                   "lic": license,
                   "q": quality,
                   "area": area,
                   "since": since,
                   "year": year,
                   "month": month}

        self.logger.debug(f"Sending request with parameters {payload}")

        r = requests.get(XC_BASE_URL, params=payload)
        r.raise_for_status()

        file_data = r.json()

        self.logger.info(f"Found {file_data['numRecordings']} recordings with "
                         f"{file_data['numSpecies']} species over "
                         f"{file_data['numPages']} pages.")

        return file_data

    def download_files(self, query: str, dir: str = "sounds"):
        """
        Downloads files returned by xeno-canto with the given search_terms.

        :param query: The terms to query xeno-canto for.
        :param dir: The name of the directory to download to.
        :return:
        """
        # Raises a FileNotFoundError if the directory does not exist.
        path = Path(dir).resolve()

        if not os.path.exists(path):
            self.logger.debug(f"Created new directory at {path}.")
            os.makedirs(path)

        file_data = self.query(query)

        # Download recording and write metadata
        for recording in file_data["recordings"]:
            with requests.get(f"http:{recording['file']}", allow_redirects=True, stream=True) as r:
                # Note that xeno-canto only supports mp3s.
                with open(f"{path / recording['id']}.mp3", "wb") as f:
                    f.write(r.content)
            self.logger.info(f"Downloaded {path / recording['id']}.")

        keys = file_data["recordings"][0].keys()

        # Save metadata
        with open(path / "metadata.csv", "w") as f:
            w = csv.DictWriter(f, keys)
            w.writeheader()
            w.writerows(file_data["recordings"])
        self.logger.info("Downloaded metadata.")
