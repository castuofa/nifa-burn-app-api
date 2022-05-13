# generated by datamodel-codegen:
#   filename:  http://web:8000/wind_direction/36.178772/-94.161357
#   timestamp: 2022-02-16T15:31:57+00:00

from __future__ import annotations
import json

from typing import Any, List, Optional, Union
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, ValidationError, validator

from app import Log
from app.models.noaa_forecasts import HourlyForecast


class _ContextItem(BaseModel):
    class Config:
        allow_population_by_field_name = True

    _version: str = Field(..., alias='@version')
    wmo_unit: str = Field(..., alias='wmoUnit')
    nws_unit: str = Field(..., alias='nwsUnit')


class Geometry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    type: str
    coordinates: List[List[List[float]]]


class Elevation(BaseModel):
    class Config:
        allow_population_by_field_name = True

    unit_code: str = Field(..., alias='unitCode')
    value: float


def parse_hours_from_interval(hour_str) -> int:
    try:
        if hour_str[0] != 'P':
            raise ValueError(f"{hour_str} must start with 'P'")

        start = hour_str[1]
        end = hour_str[-1]
        hours = 0
        if 'M' and 'S' in hour_str:
            # Example: PT1H50M49S
            # Round up in this case
            hours = int(hour_str[hour_str.index('T') + 1:hour_str.index('H')]) + 1
            # raise ValueError(f"Can't parse {hour_str}")
        elif start == 'T':
            # these are hourly intervals
            hours = int(hour_str[hour_str.index('T') + 1:hour_str.index('H')])
        elif end == 'D':
            hours = int(hour_str[1:hour_str.index('D')]) * 24
        elif 'T' and 'D' in hour_str:
            hours = int(hour_str[1:hour_str.index('D')]) * 24
            hours += int(hour_str[hour_str.index('T') + 1:hour_str.index('H')])
        else:
            raise ValueError(f"can't parse unexpected {hour_str}")
    except ValueError as exc:
        Log.info(hour_str)
        Log.error(exc)
        raise exc
    else:
        return hours


class MeasuredValueAtInterval(BaseModel):
    class Config:
        allow_population_by_field_name = True

    valid_time: str = Field(..., alias='validTime')
    value: Optional[Union[int, float]]

    @validator('valid_time')
    def validate_valid_time(cls, v):
        time_str, hour_str = v.split("/")
        # hour_val = int(hour_str[:-1])
        hours = parse_hours_from_interval(hour_str)
        date_objects = []
        for x in range(0, hours):
            date_objects.append(datetime.fromisoformat(time_str) + timedelta(hours=x))
        return date_objects
        # date_objects = [date_obj]
        # for x in range(1, hour_val + 1):
            # Increment one hour
            # date_objects.append(date_obj + timedelta(seconds=60 * 60 * x))
        # return date_objects

class Value(MeasuredValueAtInterval):
    class Config:
        allow_population_by_field_name = True

    value: float


class Temperature(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value]


class Value1(Value):
    pass


class Dewpoint(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value1]


class Value2(Value):
    pass


class MaxTemperature(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value2]


class Value3(Value):
    pass


class MinTemperature(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value3]


class RelativeHumidity(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[MeasuredValueAtInterval]


class Value5(Value):
    pass


class ApparentTemperature(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value5]


class Value6(MeasuredValueAtInterval):
    class Config:
        allow_population_by_field_name = True

    value: Any


class HeatIndex(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value6]


class Value7(MeasuredValueAtInterval):
    class Config:
        allow_population_by_field_name = True

    value: Optional[float]


class WindChill(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value7]


class Value8(MeasuredValueAtInterval):
    pass


class SkyCover(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value8]


class Value9(MeasuredValueAtInterval):
    pass


class WindDirection(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value9]


class Value10(Value):
    pass


class WindSpeed(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value10]


class Value11(Value):
    pass


class WindGust(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value11]


class Visibility(BaseModel):
    class Config:
        allow_population_by_field_name = True

    unit_code: str = Field(..., alias='unitCode')
    value: Any


class ValueItem(BaseModel):
    class Config:
        allow_population_by_field_name = True

    coverage: Optional[str]
    weather: Optional[str]
    intensity: Optional[str]
    visibility: Visibility
    attributes: List


class Value12(MeasuredValueAtInterval):
    class Config:
        allow_population_by_field_name = True

    value: List[ValueItem]


class Weather(BaseModel):
    class Config:
        allow_population_by_field_name = True

    values: List[Value12]


class ValueItem1(BaseModel):
    class Config:
        allow_population_by_field_name = True

    phenomenon: str
    significance: str
    event_number: Any


class Value13(MeasuredValueAtInterval):
    class Config:
        allow_population_by_field_name = True

    value: List[ValueItem1]


class Hazards(BaseModel):
    class Config:
        allow_population_by_field_name = True

    values: List[Value13]


class Value14(MeasuredValueAtInterval):
    pass


class ProbabilityOfPrecipitation(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value14]


class Value15(Value):
    pass


class QuantitativePrecipitation(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value15]


class Value16(MeasuredValueAtInterval):
    pass


class IceAccumulation(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value16]


class Value17(MeasuredValueAtInterval):
    pass


class SnowfallAmount(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value17]


class SnowLevel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    values: List


class CeilingHeight(SnowLevel):
    pass


class Visibility1(SnowLevel):
    pass


class Value18(Value):
    pass


class TransportWindSpeed(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value18]


class Value19(MeasuredValueAtInterval):
    pass


class TransportWindDirection(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value19]


class Value20(Value):
    pass


class MixingHeight(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value20]


class Value21(MeasuredValueAtInterval):
    pass


class HainesIndex(BaseModel):
    class Config:
        allow_population_by_field_name = True

    values: List[Value21]


class Value22(MeasuredValueAtInterval):
    pass


class LightningActivityLevel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    values: List[Value22]


class Value23(Value):
    pass


class TwentyFootWindSpeed(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value23]


class Value24(MeasuredValueAtInterval):
    pass


class TwentyFootWindDirection(BaseModel):
    class Config:
        allow_population_by_field_name = True

    uom: str
    values: List[Value24]


class WaveHeight(SnowLevel):
    pass


class WavePeriod(SnowLevel):
    pass


class WaveDirection(SnowLevel):
    pass


class PrimarySwellHeight(SnowLevel):
    pass


class PrimarySwellDirection(SnowLevel):
    pass


class SecondarySwellHeight(SnowLevel):
    pass


class SecondarySwellDirection(SnowLevel):
    pass


class WavePeriod2(SnowLevel):
    pass


class WindWaveHeight(SnowLevel):
    pass


class DispersionIndex(SnowLevel):
    pass


class Pressure(SnowLevel):
    pass


class ProbabilityOfTropicalStormWinds(SnowLevel):
    pass


class ProbabilityOfHurricaneWinds(SnowLevel):
    pass


class PotentialOf15mphWinds(SnowLevel):
    pass


class PotentialOf25mphWinds(SnowLevel):
    pass


class PotentialOf35mphWinds(SnowLevel):
    pass


class PotentialOf45mphWinds(SnowLevel):
    pass


class PotentialOf20mphWindGusts(SnowLevel):
    pass


class PotentialOf30mphWindGusts(SnowLevel):
    pass


class PotentialOf40mphWindGusts(SnowLevel):
    pass


class PotentialOf50mphWindGusts(SnowLevel):
    pass


class PotentialOf60mphWindGusts(SnowLevel):
    pass


class GrasslandFireDangerIndex(SnowLevel):
    pass


class ProbabilityOfThunder(SnowLevel):
    pass


class DavisStabilityIndex(SnowLevel):
    pass


class AtmosphericDispersionIndex(SnowLevel):
    pass


class LowVisibilityOccurrenceRiskIndex(SnowLevel):
    pass


class Stability(SnowLevel):
    pass


class RedFlagThreatIndex(SnowLevel):
    pass


class Properties(BaseModel):
    class Config:
        allow_population_by_field_name = True

    _id: str = Field(..., alias='@id')
    _type: str = Field(..., alias='@type')
    update_time: str = Field(..., alias='updateTime')
    valid_times: str = Field(..., alias='validTimes')
    elevation: Elevation
    forecast_office: str = Field(..., alias='forecastOffice')
    grid_id: str = Field(..., alias='gridId')
    grid_x: str = Field(..., alias='gridX')
    grid_y: str = Field(..., alias='gridY')
    temperature: Temperature
    dewpoint: Dewpoint
    max_temperature: MaxTemperature = Field(..., alias='maxTemperature')
    min_temperature: MinTemperature = Field(..., alias='minTemperature')
    relative_humidity: RelativeHumidity = Field(..., alias='relativeHumidity')
    apparent_temperature: ApparentTemperature = Field(..., alias='apparentTemperature')
    heat_index: HeatIndex = Field(..., alias='heatIndex')
    wind_chill: WindChill = Field(..., alias='windChill')
    sky_cover: SkyCover = Field(..., alias='skyCover')
    wind_direction: WindDirection = Field(..., alias='windDirection')
    wind_speed: WindSpeed = Field(..., alias='windSpeed')
    wind_gust: WindGust = Field(..., alias='windGust')
    weather: Weather
    hazards: Hazards
    probability_of_precipitation: ProbabilityOfPrecipitation = Field(
        ..., alias='probabilityOfPrecipitation'
    )
    quantitative_precipitation: QuantitativePrecipitation = Field(
        ..., alias='quantitativePrecipitation'
    )
    ice_accumulation: IceAccumulation = Field(..., alias='iceAccumulation')
    snowfall_amount: SnowfallAmount = Field(..., alias='snowfallAmount')
    snow_level: SnowLevel = Field(..., alias='snowLevel')
    ceiling_height: CeilingHeight = Field(..., alias='ceilingHeight')
    visibility: Visibility1
    transport_wind_speed: TransportWindSpeed = Field(..., alias='transportWindSpeed')
    transport_wind_direction: TransportWindDirection = Field(
        ..., alias='transportWindDirection'
    )
    mixing_height: MixingHeight = Field(..., alias='mixingHeight')
    haines_index: HainesIndex = Field(..., alias='hainesIndex')
    lightning_activity_level: LightningActivityLevel = Field(
        ..., alias='lightningActivityLevel'
    )
    twenty_foot_wind_speed: TwentyFootWindSpeed = Field(
        ..., alias='twentyFootWindSpeed'
    )
    twenty_foot_wind_direction: TwentyFootWindDirection = Field(
        ..., alias='twentyFootWindDirection'
    )
    wave_height: WaveHeight = Field(..., alias='waveHeight')
    wave_period: WavePeriod = Field(..., alias='wavePeriod')
    wave_direction: WaveDirection = Field(..., alias='waveDirection')
    primary_swell_height: PrimarySwellHeight = Field(..., alias='primarySwellHeight')
    primary_swell_direction: PrimarySwellDirection = Field(
        ..., alias='primarySwellDirection'
    )
    secondary_swell_height: SecondarySwellHeight = Field(
        ..., alias='secondarySwellHeight'
    )
    secondary_swell_direction: SecondarySwellDirection = Field(
        ..., alias='secondarySwellDirection'
    )
    wave_period2: WavePeriod2 = Field(..., alias='wavePeriod2')
    wind_wave_height: WindWaveHeight = Field(..., alias='windWaveHeight')
    dispersion_index: DispersionIndex = Field(..., alias='dispersionIndex')
    pressure: Pressure
    probability_of_tropical_storm_winds: ProbabilityOfTropicalStormWinds = Field(
        ..., alias='probabilityOfTropicalStormWinds'
    )
    probability_of_hurricane_winds: ProbabilityOfHurricaneWinds = Field(
        ..., alias='probabilityOfHurricaneWinds'
    )
    potential_of15mph_winds: PotentialOf15mphWinds = Field(
        ..., alias='potentialOf15mphWinds'
    )
    potential_of25mph_winds: PotentialOf25mphWinds = Field(
        ..., alias='potentialOf25mphWinds'
    )
    potential_of35mph_winds: PotentialOf35mphWinds = Field(
        ..., alias='potentialOf35mphWinds'
    )
    potential_of45mph_winds: PotentialOf45mphWinds = Field(
        ..., alias='potentialOf45mphWinds'
    )
    potential_of20mph_wind_gusts: PotentialOf20mphWindGusts = Field(
        ..., alias='potentialOf20mphWindGusts'
    )
    potential_of30mph_wind_gusts: PotentialOf30mphWindGusts = Field(
        ..., alias='potentialOf30mphWindGusts'
    )
    potential_of40mph_wind_gusts: PotentialOf40mphWindGusts = Field(
        ..., alias='potentialOf40mphWindGusts'
    )
    potential_of50mph_wind_gusts: PotentialOf50mphWindGusts = Field(
        ..., alias='potentialOf50mphWindGusts'
    )
    potential_of60mph_wind_gusts: PotentialOf60mphWindGusts = Field(
        ..., alias='potentialOf60mphWindGusts'
    )
    grassland_fire_danger_index: GrasslandFireDangerIndex = Field(
        ..., alias='grasslandFireDangerIndex'
    )
    probability_of_thunder: ProbabilityOfThunder = Field(
        ..., alias='probabilityOfThunder'
    )
    davis_stability_index: DavisStabilityIndex = Field(..., alias='davisStabilityIndex')
    atmospheric_dispersion_index: AtmosphericDispersionIndex = Field(
        ..., alias='atmosphericDispersionIndex'
    )
    low_visibility_occurrence_risk_index: LowVisibilityOccurrenceRiskIndex = Field(
        ..., alias='lowVisibilityOccurrenceRiskIndex'
    )
    stability: Stability
    red_flag_threat_index: RedFlagThreatIndex = Field(..., alias='redFlagThreatIndex')


class NOAAGridModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    _context: List[Union[str, _ContextItem]] = Field(..., alias='@context')
    id: str
    type: str
    geometry: Geometry
    properties: Properties
    forecasts: Union[HourlyForecast, None] = None

    @classmethod
    def from_response(cls, json_response: dict, station_id: str):

        grid_model = cls.parse_obj(json_response)

        speeds = {}

        humidity = {}
        features = []

        count = 0
        num_hours = 48

        try:
            for val in grid_model.properties.relative_humidity.values:
                for date_obj in val.valid_time:
                    if count >= num_hours:
                        break
                    humidity[date_obj] = val.value
                    count += 1
                if count >= num_hours:
                    break
        except Exception as exc:
            Log.error(exc)
            raise exc

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

        for val in grid_model.properties.wind_direction.values:
            for date_obj in val.valid_time:
                noaa_hourly_forecast = {
                    "station": station_id,
                    "timestamp": date_obj,
                    "wind_direction": val.value,
                    "wind_speed": speeds.get(date_obj, None),
                    "relative_humidity": humidity.get(date_obj, None)
                }
                # intervals[date_obj] = sector_feature
                features.append(HourlyForecast.parse_obj(noaa_hourly_forecast))
                hourly_iteration += 1
                count += 1
                if count >= num_hours:
                    break
            if count >= num_hours:
                break

        grid_model.forecasts = features
        return grid_model
