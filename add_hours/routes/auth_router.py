import os

from fastapi import APIRouter

router_activity = APIRouter(
    prefix=os.getenv("API_AUTH_PREFIX", "/auth"), tags=["Auth"]
)
