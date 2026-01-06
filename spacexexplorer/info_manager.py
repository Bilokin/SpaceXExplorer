import os
import json
import pathlib

import spacexpy


class InfoManager(object):
    """InfoManager class that retrieves SpaceX data"""

    def __init__(self, location: str = "./"):
        self.spacex = spacexpy.SpaceX()
        self.location = pathlib.Path(location)
        self.static_file_dict = {'company': self.spacex.request_company,
                                 'launches': self.spacex.request_launches,
                                 'landpads':  self.spacex.request_landpads,
                                 'rockets': self.spacex.request_rockets
                                 }

    def fetch_static(self):
        """
        Fetches the requested information from SpaceX API and
        stores it in JSON files for further use
        """
        for filename in self.static_file_dict:
            with open(self.location / f'{filename}.json', 'w') as f:
                data = self.static_file_dict[filename]()
                json.dump(data, f, indent='    ')

    def get(self, info_type: str, **kw_args) -> object:
        """
        Returns info from static or dynamic sources
        """
        if info_type in self.static_file_dict:
            path = self.location / f'{info_type}.json'
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f'File {path} not available, please run fetch_static()')
            with open(path, 'r') as f:
                return json.load(f)

    def save_static(self, destination: str):
        """
        Copies static files to desctination
        """
        pass
