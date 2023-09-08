import io
import os
from typing import Annotated, Optional

from bson.objectid import ObjectId
from fastapi import (
    APIRouter, HTTPException, Query, UploadFile
)

from add_hours.application.dto.request.activity import (
    ActivityRequest,
)
from add_hours.application.dto.response.activity import (
    ActivitySaveResponse, GetActivitiesResponse,
)
from add_hours.application.services.activity_service import ActivityService
from add_hours.application.services.storage_service import StorageService

router_activity = APIRouter(
    prefix=os.getenv("API_ACTIVITY_PREFIX", "/activity"), tags=["Activity"]
)


@router_activity.post("/", status_code=201, response_model=ActivitySaveResponse)
async def save_activity(activity_request: ActivityRequest):
    response = await ActivityService.save_activity(activity_request)
    return response


@router_activity.post(
    "/certificate/{student_id}/{activity_id}", status_code=201
)
async def save_certificate(
    student_id: str, activity_id: str, certificate: UploadFile
):
    if not ObjectId.is_valid(student_id) or not ObjectId.is_valid(activity_id):
        # TODO: Excessão temporária
        raise HTTPException(status_code=422, detail="Invalid object id")

    certificate_name = certificate.filename
    if not certificate.content_type == os.getenv(
            "MINIO_SUPPORTED_MIME_TYPE", "application/pdf"
    ):
        raise HTTPException(status_code=422, detail="Invalid file format")

    await StorageService.save_certificate(
        certificate_name, student_id, activity_id,
        io.BytesIO(await certificate.read())
    )


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

# @router_activity.delete("/{activity_id}", status_code=204)
# async def delete_activity(activity_id: str):
#     await ActivityService.delete_activity(activity_id)


# @router_activity.put("/{device_id}", status_code=200)
# async def update_device(device_id: str, update_request: ActivityRequest):
#     pass
