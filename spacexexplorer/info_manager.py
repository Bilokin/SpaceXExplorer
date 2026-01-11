import os
import sys
import json
import pathlib
from typing import Any
import spacexpy

from aiohttp.client_exceptions import ClientConnectorError


class InfoManager(object):
    """InfoManager class that retrieves SpaceX data"""

    def __init__(self, location: str = "./"):
        self.spacex = spacexpy.SpaceX()
        self.location = pathlib.Path(location)
        self.static_file_dict = {"company": self.spacex.request_company,
                                 "landpads":  self.spacex.request_landpads,
                                 "launchpads":  self.spacex.request_launchpads,
                                 "rockets": self.spacex.request_rockets,
                                 "launches": self.spacex.request_launches  # keep as last one for statistics
                                 }
        self.launchpad_info: dict = {}
        self.rocket_info: dict = {}
        self.launch_stats: dict = {"years": {}, "months": {}}

    def record_launch(self, launch: dict) -> None:
        """
        Records launch stats
        """
        if launch['success']:
            self.launchpad_info[launch['launchpad']
                                ]['successful_launches'] += 1
            self.rocket_info[launch['rocket']
                                ]['successful_launches'] += 1
        self.launchpad_info[launch['launchpad']
                            ]['total_launches'] += 1
        self.rocket_info[launch['rocket']
                            ]['total_launches'] += 1
        year, month, _ = launch["date_utc"].split('T')[0].split('-')
        year = int(year)
        month = int(month)
        if year in self.launch_stats["years"]:
            self.launch_stats["years"][year] += 1
        else:
            self.launch_stats["years"][year] = 1
        if month in self.launch_stats["months"]:
            self.launch_stats["months"][month] += 1
        else:
            self.launch_stats["months"][month] = 1

    def fetch_static(self) -> None:
        """
        Fetches the requested information from SpaceX API and
        stores it in JSON files for further use
        """
        try:
            for filename in self.static_file_dict:
                with open(self.location / f'{filename}.json', 'w') as f:
                    data = self.static_file_dict[filename]()
                    json.dump(data, f, indent='    ')
                    if filename == "launchpads":
                        for launchpad in data:
                            self.launchpad_info[launchpad["id"]
                                                ] = {"name": launchpad.get("full_name"),
                                                     "successful_launches": 0,
                                                     "total_launches": 0}
                    if filename == "rockets":
                        for rocket in data:
                            self.rocket_info[rocket["id"]] = {"name": rocket.get("name"),
                                                              "successful_launches": 0,
                                                              "total_launches": 0}
                    if filename == "launches":
                        for launch in data:
                            self.record_launch(launch)
        except ClientConnectorError:
            sys.exit(
                "No access to SpaceX API, please check your internet connection!")

    def get(self, info_type: str, **kw_args) -> Any:
        """
        Returns info from static or dynamic sources
        """
        if info_type in self.static_file_dict:
            path = self.location / f'{info_type}.json'
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f'File {path} not available, please relaunch the program')
            with open(path, 'r') as f:
                return json.load(f)
        else:
            raise NotImplementedError()

    def filter_launches(self, **filters) -> list:
        """
        Filters the launch list
        """
        info = self.get("launches")
        if len(filters) < 1:
            return info
        filtered = []
        for launch in info:
            accepted = True
            for key in filters:
                if launch[key] != filters[key]:
                    accepted = False
                    break
            if accepted:
                filtered.append(launch)
        return filtered

    def save_static(self, destination: str):
        """
        Copies static files to desctination
        """
        pass
