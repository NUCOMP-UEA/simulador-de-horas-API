# import os
#
# from fastapi import APIRouter
#
# from add_hours.application.services.storage_service import StorageService
#
# router_certificate = APIRouter(
#     prefix=os.getenv("API_CERTIFICATE_PREFIX", "/certificate"),
#     tags=["Certificate"]
# )
#
#
# @router_certificate.get("/{student_id}/{activity_id}", status_code=200)
# async def get_certificates(student_id: str, activity_id: str):
#     return await StorageService.get_certificates(student_id, activity_id)
