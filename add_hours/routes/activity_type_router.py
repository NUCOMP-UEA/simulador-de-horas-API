import os
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Response
from fastapi.security import OAuth2PasswordBearer

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router_activity_type.post("/", status_code=201)
async def save_activity_type(
    activity_type_request: ActivityTypeRequest,
    _: Annotated[str, Depends(oauth2_scheme)],
):
    await ActivityTypeService.save_activity_type(activity_type_request)
    return Response(status_code=201)


@router_activity_type.get(
    "/", status_code=200, response_model=list[ActivityTypeSearchResponse]
)
async def get_activity_types(
    search: Annotated[Optional[str], Query()] = None,
):
    return await ActivityTypeService.search_activity_type(search)


@router_activity_type.put("/{activity_type_id}", status_code=200)
async def update_activity_type(
    activity_type_id: str,
    activity_type_request: ActivityTypeRequest,
    _: Annotated[str, Depends(oauth2_scheme)],
):
    return await ActivityTypeService.update_activity_type(
        activity_type_id, activity_type_request
    )


@router_activity_type.delete("/{activity_type_id}", status_code=204)
async def delete_activity_type(
    activity_type_id: str,
    _: Annotated[str, Depends(oauth2_scheme)],
):
    return await ActivityTypeService.delete_activity_type(activity_type_id)
