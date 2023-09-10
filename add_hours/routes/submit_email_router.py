import os

from fastapi import APIRouter

from add_hours.application.services.submit_service import SubmitService

router_submit = APIRouter(
    prefix=os.getenv("API_SUBMIT_PREFIX", "/submit"),
    tags=["Submit"]
)


@router_submit.post("/{student_id}", status_code=200)
async def submit_email(student_id: str):
    return await SubmitService.submit_email(student_id)
