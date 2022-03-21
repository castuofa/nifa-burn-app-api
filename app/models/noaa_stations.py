from typing import Union
from datetime import datetime
import ormar
from pydantic import AnyHttpUrl

from app.database.connection import BaseMeta
from .geom import GeoJSONGeometryType, OrmarGeoJSON


class NoaaStations(ormar.Model):

    grid_id: str = ormar.String(max_length=25, primary_key=True)
    forecast_office_url: AnyHttpUrl = ormar.String(max_length=255)
    grid_x: int = ormar.Integer()
    grid_y: int = ormar.Integer()
    forecast_url: AnyHttpUrl = ormar.String(max_length=255)
    forecast_hourly_url: AnyHttpUrl = ormar.String(max_length=255)
    forecast_grid_data_url: AnyHttpUrl = ormar.String(max_length=255)
    observation_stations_url: AnyHttpUrl = ormar.String(max_length=255)
    geometry: GeoJSONGeometryType = OrmarGeoJSON(shape="POLYGON", srid=4326)
    collected_at: Union[datetime, None] = ormar.DateTime(
        nullable=True, default=datetime.now
    )

    class Meta(BaseMeta):
        tablename = "noaa_stations"

    @classmethod
    async def from_response(cls, data: dict):
        parsed_object = {
            "grid_id": data.get("gridId")
                + "_"
                + str(data.get("gridX"))
                + "_"
                + str(data.get("gridY")),
            "grid_x": data.get("gridX"),
            "grid_y": data.get("gridY"),
            "forecast_office_url": data.get("forecastOffice"),
            "forecast_url": data.get("forecast"),
            "forecast_hourly_url": data.get("forecastHourly"),
            "forecast_grid_data_url": data.get("forecastGridData"),
            "observation_stations_url": data.get("observationStations"),
            "geometry": data.get("geometry"),
        }

        model = await cls.objects.get_or_none(grid_id=parsed_object.get("grid_id"))
        if not model:
            model = await cls.objects.create(**parsed_object)
        else:
            await model.update(**parsed_object)
        return model

@ormar.pre_update(NoaaStations)
@ormar.pre_save(NoaaStations)
async def before_update_and_save(sender, instance: NoaaStations, **kwargs):
    instance.collected_at = datetime.now()
