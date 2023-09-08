import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from add_hours.application.services.auth_service import AuthService

router_auth = APIRouter(
    prefix=os.getenv("API_AUTH_PREFIX", "/auth"), tags=["Auth"]
)


@router_auth.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    form_data_is_valid = await AuthService.verify_user(
        form_data.username, SecretStr(form_data.password)
    )

    if not form_data_is_valid:
        # TODO: Exception temporária
        raise HTTPException(status_code=401, detail="Invalid credentials")
