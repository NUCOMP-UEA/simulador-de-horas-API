import os
from typing import Optional

from fastapi import APIRouter, Query, Response
from pydantic import Field

from add_hours.application.dto.request.activity import (
    ActivityRequest,
    ActivityUpdateRequest,
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


@router_activity.get("/", status_code=200, response_model=GetActivitiesResponse)
async def get_activities(
    current_page: Optional[int] = Query(default=1, alias="currentPage"),
    page_size: Optional[int] = Query(default=10, alias="pageSize"),
):
    return await ActivityService.get_activities(current_page, page_size)


@router_activity.delete("/{activity_id}", status_code=204)
async def delete_activity(activity_id: str):
    await ActivityService.delete_activity(activity_id)
    return Response(status_code=204)


@router_activity.put("/{device_id}", status_code=200)
async def update_device(device_id: str, update_request: ActivityUpdateRequest):
    pass
