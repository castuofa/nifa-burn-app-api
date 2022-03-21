from datetime import datetime
from typing import Union

import ormar
from pydantic import root_validator

from app.database.connection import BaseMeta
from .noaa_stations import NoaaStations


class HourlyForecast(ormar.Model):

    id: str = ormar.String(primary_key=True, max_length=255)
    station: str = ormar.ForeignKey(to=NoaaStations, nullable=False)
    timestamp: datetime = ormar.DateTime()
    wind_direction: int = ormar.Integer()
    wind_speed: float = ormar.Float()
    collected_at: Union[datetime, None] = ormar.DateTime(nullable=True, default=datetime.now)

    @root_validator(pre=True)
    def id_should_be_combined_from_grid_id_and_timstamp(cls, values):
        if values.get('id'):
            assert values.get('id') == values.get('station').grid_id + "_" + str(values.get('timestamp'))
        else:
            values['id'] = values.get('station').grid_id + "_" + str(values.get('timestamp'))
        return values

    class Meta(BaseMeta):
        constraints = [ormar.UniqueColumns("station", "timestamp", name="uniq_hourlyforecasts_station_timestamp")]


@ormar.pre_update(HourlyForecast)
@ormar.pre_save(HourlyForecast)
async def before_update_and_save(sender, instance: HourlyForecast, **kwargs):
    instance.collected_at = datetime.now()