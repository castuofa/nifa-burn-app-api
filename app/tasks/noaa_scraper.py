from datetime import datetime, timedelta
import asyncio
import geojson

import ormar
import aiohttp
from pydantic import ValidationError

from app import storage
from app.models.noaa_grid import NOAAGridModel
from app.models.noaa_stations import NoaaStations
from app.database.connection import database
from app import Log


class Task:

    signature: str = "base.task"

    def __init__(self, *args, **kwargs):
        Log.info(f"Starting {self.signature}")

    async def handle(self, loop=None):
        Log.info("Should not see this")

    @classmethod
    async def runner(cls):
        instance = cls()
        await instance.handle()


async def get_forecast(session, station, retry=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
    }
    async with session.get(station.forecast_grid_data_url, headers=headers) as response:
        try:
            json_data = await response.json()

            if json_data.get("status", None) == 500:
                raise ValueError(f"Bad return: {json_data.get('detail', None)}")

            grid_model = NOAAGridModel.from_response(
                json_data, station_id=station.grid_id
            )
        except (ValueError, ValidationError) as exc:
            Log.error(exc)

            # Log.error(
            #     f"TRY {retry} Bad return: {station.grid_id} | {station.forecast_grid_data_url}"
            # )
            return None
        else:
            # Log.info(
            #     f"TRY {retry} Success: {station.grid_id} | {station.forecast_grid_data_url}"
            # )
            return grid_model


class NOAA_ForecastCollector(Task):

    signature: str = "noaa.forecast_collect"

    description: str = "Collect forecast data from all stations"

    async def collect_and_process(self, session, station):
        grid_model = None

        retry_count = 0
        while not grid_model:
            grid_model = await get_forecast(session, station, retry=retry_count)
            retry_count += 1
            if not grid_model:
                await asyncio.sleep(0.1)
            if retry_count >= 10:
                Log.info(f"Missed: {station}")
                break

        if not grid_model:
            return None

        forecast_count = 0
        Log.info(f"Saving forecasts...")
        for forecast in grid_model.forecasts:
            try:
                await forecast.load()
                await forecast.update()
            except ormar.exceptions.NoMatch:
                await forecast.save()
            finally:
                await forecast.station.update()
            forecast_count += 1
        Log.info(f"{forecast_count} forecasts saved successfully")

        return None


    async def handle(self, loop=None):
        Log.info(f"{self.signature}: Running hanlder")

        loop = loop if loop else asyncio.get_running_loop()

        await database.connect()
        time_check = datetime.now() - timedelta(hours=12)
        stations = await NoaaStations.objects.filter(collected_at__lte=time_check).all()
        async with aiohttp.ClientSession(loop=loop) as session:
            Log.info(f"{self.signature}: collecting requests...")
            requests = []

            for station in stations:

                requests.append(loop.create_task(self.collect_and_process(session, station)))

                if len(requests) >= 20:
                    Log.info(f"{self.signature}: starting {len(requests)} requests...")
                    results = await asyncio.gather(*requests, return_exceptions=True)
                    Log.info(f"{results}")
                    requests = []

            if requests:
                Log.info(f"{self.signature}: starting {len(requests)} requests...")
                results = await asyncio.gather(*requests, return_exceptions=True)
                Log.info(f"{results}")

        await database.disconnect()
        Log.info(f"{self.signature}: Completed handler")

    @classmethod
    async def runner(cls):
        instance = cls()
        await instance.handle()


class NOAA_GridUpdater(Task):

    signature: str = "noaa.grid_update"

    description: str = "Update relevant grid points based on their timestamp."

    async def handle(self, loop=None):
        await database.connect()

        stations = await NoaaStations.objects.filter(collected_at=None).all()

        Log.info(f"Updating {len(stations)} NoaaStation records")
        for station in stations:
            async with aiohttp.ClientSession() as session:
                grid_url = station.forecast_grid_data_url
                async with session.get(grid_url) as response:
                    json_response = await response.json()
                    if json_response.get("status", 200) == 500:
                        Log.error(f"API failed for {grid_url}")
                        continue
                    await station.update(geometry=json_response.get("geometry", None))

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
        self.errored = 0
        with self.json_file_path.open("r") as raw_file:
            self.file_data = geojson.load(raw_file)
        self.total = 0
        self.expected = len(self.file_data["features"])
        Log.info(f"Expecting: {self.expected }")

    async def collect_and_process(self, session, url):
        try:
            station_data = await self.get_point(
                session, url
            )
        except ValueError as exc:
            Log.error(exc)
            self.errored += 1
        else:
            await NoaaStations.from_response(station_data)

        self.total += 1
        Log.info(f"{self.total}/{self.expected} Completed from: {url}")

    async def handle(self, loop=None):
        loop = asyncio.get_running_loop() if not loop else loop

        await database.connect()
        points = map(
            lambda obj: obj["geometry"]["coordinates"], self.file_data["features"]
        )

        async with aiohttp.ClientSession(loop=loop) as session:

            request_list = []

            for _, pnt in enumerate(points):

                url = self.base_url.format(pnt[1], pnt[0])

                request_list.append(loop.create_task(self.collect_and_process(session, url)))

            Log.info(f"Sending requests...")
            await asyncio.gather(*request_list, return_exceptions=True)

        await database.disconnect()
        Log.info(f"Collected {self.total} of {self.expected}")
        if self.errored > 0:
            Log.error(f"Unable to collect from {self.errored} urls")

    @staticmethod
    async def get_point(session, url):
        station_data = {}
        async with session.get(url) as response:
            json_response = await response.json()
            if json_response.get("status", 200) == 500:
                raise ValueError(f"API Failure {url}")
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
