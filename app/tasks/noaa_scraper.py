from datetime import datetime, timedelta
import json
import geojson

import aiohttp
from app import storage
from app.models.geom import GeometryType
from app.models.noaa_grid import NOAAGridModel
from app.models.noaa_stations import NoaaStations
from app.database.connection import database
from app import Log


class Task:

    signature: str = "base.task"

    def __init__(self, *args, **kwargs):
        Log.info(f"Starting {self.signature}")

    async def handle(self):
        pass

    @classmethod
    async def runner(cls):
        instance = cls()
        await instance.handle()


class NOAA_ForecastCollector(Task):

    signature: str = "noaa.forecast_collect"

    description: str = "Collect forecast data from all stations"

    async def handle(self):
        await database.connect()
        time_check = datetime.now() - timedelta(hours=12)
        stations = await NoaaStations.objects.filter(
            collected_at__lte = time_check
        ).first()

        # for station in stations:
        async with aiohttp.ClientSession() as session:
            async with session.get(stations.forecast_grid_data_url) as response:
                print(NOAAGridModel.from_response(await response.json(), station_id=stations.grid_id))


        await database.disconnect()

    @classmethod
    async def runner(cls):
        instance = cls()
        await instance.handle()


class NOAA_GridUpdater(Task):

    signature: str = "noaa.grid_update"

    description: str = "Update relevant grid points based on their timestamp"

    async def handle(self):
        await database.connect()

        stations = await NoaaStations.objects.filter(
            collected_at = None
        ).all()

        Log.info(f"Updating {len(stations)} NoaaStation records")
        for station in stations:
            async with aiohttp.ClientSession() as session:
                grid_url = station.forecast_grid_data_url
                async with session.get(grid_url) as response:
                    json_response = await response.json()
                    if json_response.get("status", 200) == 500:
                        Log.error(f"API failed for {grid_url}")
                        continue
                    await station.update(geometry = json_response.get("geometry", None))

        await database.disconnect()

    @classmethod
    async def runner(cls):
        instance = cls()
        await instance.handle()

class NOAA_Grid(Task):

    signature: str = "noaa.grid_collector"

    description: str = "Collect relevant grid points based on point grid geojson file"

    json_file_path = storage("assets/point_grid_12_5km.geojson")

    base_url: str = "https://api.weather.gov/points/{0},{1}"

    def __init__(self):
        super().__init__()
        with self.json_file_path.open("r") as raw_file:
            self.file_data = geojson.load(raw_file)
        self.total = 0
        self.expected = len(self.file_data['features'])
        Log.info(f"Expecting: {self.expected }")

    async def handle(self):
        await database.connect()
        points = map(lambda obj: obj["geometry"]["coordinates"], self.file_data["features"])
        async with aiohttp.ClientSession() as session:
            for _, pnt in enumerate(points):

                try:
                    station_data = await self.get_point(session, self.base_url.format(pnt[1], pnt[0]))
                except ValueError:
                    continue
                self.total += 1
                await NoaaStations.from_response(station_data)

        await database.disconnect()
        Log.info(f"Collected {self.total} of {self.expected}")

    @staticmethod
    async def get_point(session, url):
        station_data = {}
        async with session.get(url) as response:
            json_response = await response.json()
            if json_response.get("status", 200) == 500:
                raise ValueError("API Failure")
            station_data = json_response.get("properties")

        grid_url = station_data.get("forecastGridData")
        async with session.get(grid_url) as response:
            json_response = await response.json()
            if json_response.get("status", 200) == 500:
                raise ValueError("API Failure")
            station_data["geometry"] = json_response.get("geometry", None)
            if not station_data.get("geometry", None):
                raise ValueError(f"Geometry still missing {grid_url}")

        return station_data