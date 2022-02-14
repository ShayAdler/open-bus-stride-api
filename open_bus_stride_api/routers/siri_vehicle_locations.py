import typing
import datetime
import sqlalchemy

import pydantic
from fastapi import APIRouter

from open_bus_stride_db.model.siri_vehicle_location import SiriVehicleLocation
from open_bus_stride_db import model

from . import siri_rides, siri_routes
from . import common


router = APIRouter()


class SiriVehicleLocationPydanticModel(pydantic.BaseModel):
    id: int
    siri_snapshot_id: int
    siri_ride_stop_id: int
    recorded_at_time: datetime.datetime
    lon: float
    lat: float
    bearing: int
    velocity: int
    distance_from_journey_start: int
    distance_from_siri_ride_stop_meters: typing.Optional[int]

siri_route_related_model = common.PydanticRelatedModel(
    'siri_route__', siri_routes.SiriRoutePydanticModel, ['id']
)
siri_ride_related_model = common.PydanticRelatedModel(
    'siri_ride__', siri_rides.SiriRidePydanticModel, ['id']
)

SiriVehicleLocationWithRelatedPydanticModel = common.pydantic_create_model_with_related(
    'SiriVehicleLocationWithRelatedPydanticModel',
    SiriVehicleLocationPydanticModel,
    siri_route_related_model,
    siri_ride_related_model,
)

def _post_session_query_hook(session_query: sqlalchemy.orm.Query):
    return (
        session_query
        .select_from(model.SiriVehicleLocation)
        .add_entity(model.SiriRide)
        .add_entity(model.SiriRoute)
        .join(model.SiriRideStop)
        .join(model.SiriRide)
        .join(model.SiriRoute, model.SiriRoute.id == model.SiriRide.siri_route_id)
    )

def _convert_to_dict(obj: model.SiriVehicleLocation):
    siri_vehicle_location, siri_ride, siri_route = obj
    res = siri_vehicle_location.__dict__
    siri_route_related_model.add_orm_obj_to_dict_res(siri_route, res)
    siri_ride_related_model.add_orm_obj_to_dict_res(siri_ride, res)
    return res

@router.get("/list", tags=['siri'], response_model=typing.List[SiriVehicleLocationWithRelatedPydanticModel])
def list_(limit: int = None, offset: int = None,
          siri_vehicle_location_ids: str = None,
          siri_snapshot_ids: str = None, siri_ride_stop_ids: str = None,
          recorded_at_time_from: datetime.datetime = None, recorded_at_time_to: datetime.datetime = None,
          order_by: str = None, siri_routes__line_ref: str = None):
    """
    * siri_vehicle_location_ids: comma-separated list
    * siri_snapshot_ids: comma-separated list
    * siri_ride_stop_ids: comma-separated list
    * recorded_at_time_from / recorded_at_time_to: YYYY-MM-DDTHH:MM:SS+Z (e.g. 2021-11-33T55:48:49+00:00)
    * order_by: comma-separated list of order by fields, e.g.: "siri_snapshot_id desc,recorded_at_time asc"
    """
    return common.get_list(
        SiriVehicleLocation, limit, offset,
        [
            {'type': 'equals', 'field': model.SiriRoute.line_ref, 'value': siri_routes__line_ref},
            {'type': 'in', 'field': SiriVehicleLocation.id, 'value': siri_vehicle_location_ids},
            {'type': 'in', 'field': SiriVehicleLocation.siri_snapshot_id, 'value': siri_snapshot_ids},
            {'type': 'in', 'field': SiriVehicleLocation.siri_ride_stop_id, 'value': siri_ride_stop_ids},
            {'type': 'datetime_from', 'field': SiriVehicleLocation.recorded_at_time, 'value': recorded_at_time_from},
            {'type': 'datetime_to', 'field': SiriVehicleLocation.recorded_at_time, 'value': recorded_at_time_to},
        ],
        order_by=order_by,
        post_session_query_hook=_post_session_query_hook,
        convert_to_dict=_convert_to_dict,
    )


@router.get('/get', tags=['siri'], response_model=SiriVehicleLocationPydanticModel)
def get_(id: int):
    return common.get_item(SiriVehicleLocation, SiriVehicleLocation.id, id)
