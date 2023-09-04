import os
from typing import Annotated, Optional

from fastapi import APIRouter, Query, Response

from add_hours.application.dto.request.activity import (
    ActivityRequest,
)
from add_hours.application.dto.response.activity import (
    GetActivitiesResponse,
)
from add_hours.application.services.activity_service import ActivityService

router_activity = APIRouter(
    prefix=os.getenv("API_ACTIVITY_PREFIX", "/activity"), tags=["Activity"]
)


@router_activity.post("/", status_code=201)
async def save_activity(activity_request: ActivityRequest):
    await ActivityService.save_activity(activity_request)
    return Response(status_code=201)


@router_activity.get(
    "/{student_id}", status_code=200, response_model=GetActivitiesResponse
)
async def get_activities(
    student_id: str,
    current_page: Annotated[Optional[int], Query(gt=0, alias="currentPage")] = 1,
    page_size: Annotated[Optional[int], Query(gt=0, alias="pageSize")] = 10,
):
    return await ActivityService.get_activities(
        student_id, current_page, page_size
    )


@router_activity.delete("/{activity_id}", status_code=204)
async def delete_activity(activity_id: str):
    await ActivityService.delete_activity(activity_id)
    return Response(status_code=204)


@router_activity.put("/{device_id}", status_code=200)
async def update_device(device_id: str, update_request: ActivityRequest):
    pass
