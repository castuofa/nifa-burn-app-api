"""
Basic public default controller
"""
from datetime import datetime, date, timedelta
from typing import Any, List, Optional
from fastapi import APIRouter, Request

# NOAA Imports
from noaa_sdk import NOAA
from pydantic import BaseModel, Field

# App Imports
from app.models.noaa_grid import NOAAGridModel
from app.models.wind_shed import WindShedCollection

# Third-party imports
from turfpy.misc import sector
from geojson import Point, Feature, FeatureCollection

# Router instance
router = APIRouter()

# Define the base URI
prefix = ""

# Define the internal tags
tags = ["api"]

#########################################################


class ForecastModel(BaseModel):

  start_time: datetime = Field(alias="startTime")
  end_time: datetime = Field(alias="endTime")
  is_day_time: bool = Field(alias="isDaytime")
  detailed_forecast: str = Field(alias="detailedForecast")
  short_forecast: str = Field(alias="shortForecast")
  name: str = Field()
  wind_speed: str = Field(alias="windSpeed")
  wind_direction: str = Field(alias="windDirection")
  temperature: int = Field()
  temperature_trend: Optional[Any] = Field(alias="temperatureTrend")
  temperature_unit: str = Field(alias="temperatureUnit")
  number: int = Field()
  icon: str = Field()


@router.get("/")
def index(request: Request):
    return {"status": "up"}


@router.get(
  "/forecast",
  response_model=list[ForecastModel],
  response_model_by_alias=False,
  description="An end point that provides access to the `forecast` API data from NOAA")
def forecast(x: float = None, y: float = None, zip: str = None, hourly: bool = False):

  valid = x and y or zip
  if not valid:
    raise ValueError("A coordinate XY pair or zip code is required")

  noaa = NOAA()

  if zip:
    return noaa.get_forecasts(zip, 'US', hourly, type='forecast')

  if x and y:
    return noaa.points_forecast(x, y, hourly, type='forecast')


@router.get(
  "/forecast/hourly",
  response_model=list[ForecastModel],
  response_model_by_alias=False,
  description="An end point that provides access to the `forecastHourly` API data from NOAA")
def forecast(x: float = None, y: float = None, zip: str = None, hourly: bool = False):

  valid = x and y or zip
  if not valid:
    raise ValueError("A coordinate XY pair or zip code is required")

  noaa = NOAA()

  if zip:
    return noaa.get_forecasts(zip, 'US', hourly, type='forecastHourly')

  if x and y:
    return noaa.points_forecast(x, y, hourly, type='forecastHourly')


@router.get(
  "/forecast/grid",
  # response_model=list[ForecastModel],
  # response_model_by_alias=False,
  description="An end point that provides access to the `forecastGridData` API data from NOAA")
def forecasts(x: float = None, y: float = None):

  valid = x and y or zip
  if not valid:
    raise ValueError("A coordinate XY pair or zip code is required")

  return NOAA().points_forecast(x, y, type='forecastGridData')


@router.get(
  "/observations",
  # response_model=list[ForecastModel],
  # response_model_by_alias=False,
  description="Provides access to the `observations` API data from NOAA given a date range. Be mindful of ranges as multiple days will return a mass of data")
def forecast(
  start_date: date = (date.today() - timedelta(4)).isoformat(),
  end_date: date = date.today().isoformat(),
  x: float = None,
  y: float = None,
  zip: str = None
):

  valid = x and y or zip
  if not valid:
    raise ValueError("A coordinate XY pair or zip code is required")

  noaa = NOAA()

  if zip:
    return noaa.get_observations(zip, 'US', start_date.isoformat(), end_date.isoformat())

  if x and y:
    return noaa.get_observations_by_lat_lon(x, y, start_date.isoformat(), end_date.isoformat())


def calculate_bearings(bearing, distance = 15):
    bisect = distance / 2
    start = bearing - bisect
    end = bearing + bisect

    if 0 <= start <= bearing <= 360:
        start = start
    else:
        start += 360

    if 0 <= bearing <= end <= 360:
        end = end
    else:
        end -= 360

    return start, end


@router.get(
    '/wind_shed/{x}/{y}',
    description="Returns a GeoJSON of hourly wind shed features for next six hours",
    response_model=WindShedCollection
)
async def wind_shed(
    x: float,
    y: float,
    shed_angle: int = 30,
    shed_distance: int = 10,
    num_hours: int = 12
):
    noaa = NOAA()

    # Get expected radius
    point = Feature(geometry=Point((y, x,)))

    grid_model = NOAAGridModel.parse_obj(
        noaa.points_forecast(x, y, hourly=True, type='forecastGridData')
    )

    speeds = {}
    intervals = {}

    count = 0

    for val in grid_model.properties.wind_speed.values:
        for date_obj in val.valid_time:
            if count >= num_hours:
                break
            speeds[date_obj] = val.value
            count += 1
        if count >= num_hours:
            break

    hourly_iteration = 1
    count = 0

    features = []

    for val in grid_model.properties.wind_direction.values:
        for date_obj in val.valid_time:
            bearing = val.value
            start_bearing, end_bearing = calculate_bearings(bearing, shed_angle)
            sector_feature = sector(
                point,
                shed_distance,
                start_bearing,
                end_bearing,
                options = {"units": "mi", "steps": 500}
            )
            sector_feature["properties"] = {
                "hourly_interval": date_obj,
                "wind_direction": val.value,
                "wind_speed": speeds.get(date_obj, None)
            }
            # intervals[date_obj] = sector_feature
            features.append(sector_feature)
            hourly_iteration += 1
            count += 1
            if count >= num_hours:
                break
        if count >= num_hours:
            break

    return FeatureCollection(features)