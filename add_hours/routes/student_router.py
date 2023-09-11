import os

from fastapi import APIRouter

from add_hours.application.dto.request.student import StudentRequest
from add_hours.application.dto.response.student import StudentResponse
from add_hours.application.services.student_service import StudentService

router_student = APIRouter(
    prefix=os.getenv("API_STUDENT_PREFIX", "/student"), tags=["Student"]
)


@router_student.post("/", status_code=201, response_model=StudentResponse)
async def save_student(student_request: StudentRequest):
    return await StudentService.save_student(student_request)


@router_student.get("/", status_code=200, response_model=list[StudentResponse])
async def get_students():
    return await StudentService.get_students()


@router_student.get(
    "/{student_id}", status_code=200, response_model=StudentResponse
)
async def get_student(student_id: str):
    return await StudentService.get_student(student_id)


# @router_student.delete("/{student_id}", status_code=204)
# async def delete_student(student_id: str):
#     await StudentService.delete_activity(student_id)
#     return Response(status_code=204)
#
#
# @router_student.put("/{student_id}", status_code=200)
# async def update_student(student_id: str, student_request: StudentRequest):
#     pass
