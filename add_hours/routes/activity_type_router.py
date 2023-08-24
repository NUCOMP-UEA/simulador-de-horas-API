import os
from typing import Optional

from fastapi import APIRouter, Query, Response


from add_hours.application.dto.request.activity import (
    ActivityTypeRequest,
)
from add_hours.application.dto.response.activity import (
    ActivityTypeSearchResponse,
)
from add_hours.application.services.activity_type_service import (
    ActivityTypeService,
)

router_activity_type = APIRouter(
    prefix=os.getenv("API_ACTIVITY_TYPE_PREFIX", "/activity/type"),
    tags=["Activity Type"],
)


@router_activity_type.post("/", status_code=201)
async def save_activity_type(activity_type_request: ActivityTypeRequest):
    await ActivityTypeService.save_activity_type(activity_type_request)
    return Response(status_code=201)


@router_activity_type.get(
    "/", status_code=200, response_model=list[ActivityTypeSearchResponse]
)
async def get_activities(search: Optional[str] = Query(default="Instrução")):
    return await ActivityTypeService.search_activity_type(search)
