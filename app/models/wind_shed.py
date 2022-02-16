# generated by datamodel-codegen:
#   filename:  http://web:8000/wind_direction/36.178772/-94.161357
#   timestamp: 2022-02-16T22:52:35+00:00

from __future__ import annotations
from datetime import datetime

from typing import List

from pydantic import BaseModel


class Geometry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type: str
    coordinates: List[List[List[float]]]


class WindShedProperties(BaseModel):
    class Config:
        allow_population_by_field_name = True

    hourly_interval: datetime
    wind_direction: int
    wind_speed: float


class Feature(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type: str
    geometry: Geometry
    properties: WindShedProperties


class WindShedCollection(BaseModel):
    class Config:
        allow_population_by_field_name = True

    features: List[Feature]
    type: str = "FeatureCollection"
