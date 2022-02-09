"""
Basic public default controller
"""
from datetime import datetime, date, timedelta
from typing import Any, List, Optional
from fastapi import APIRouter, Request

# NOAA Imports
from noaa_sdk import NOAA
from pydantic import BaseModel, Field

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
def forecast(x: float = None, y: float = None, zip: str = None):

  valid = x and y or zip
  if not valid:
    raise ValueError("A coordinate XY pair or zip code is required")

  noaa = NOAA()

  if zip:
    return noaa.get_forecasts(zip, 'US', type='forecastGridData')

  if x and y:
    return noaa.points_forecast(x, y, type='forecastGridData')


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

