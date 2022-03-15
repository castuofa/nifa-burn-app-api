import geojson
import aiohttp

from app import storage


class NOAA_Grid:

    name: str = "noaa.grid_collector"

    description: str = "Collect relevant grid points based on point grid geojson file"

    json_file_path = storage("assets/point_grid_12_5km.geojson")

    def __init__(self):
        print(self.json_file_path.exists())
        with self.json_file_path.open("r") as raw_file:
            self.file_data = geojson.load(raw_file)

    async def handle(self):
        points = map(lambda obj: obj["geometry"]["coordinates"], self.file_data["features"])
        for pnt in points:
            print(pnt[0], pnt[1])