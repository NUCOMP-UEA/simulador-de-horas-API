import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from add_hours.application.dto.response.auth import TokenResponse

router_auth = APIRouter(
    prefix=os.getenv("API_AUTH_PREFIX", "/auth"), tags=["Auth"]
)


@router_auth.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    access_token_expires = timedelta(
        minutes=int(os.getenv("AUTH_EXPIRE_MINUTES"))
    )
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )
    # return {"access_token": access_token, "token_type": "bearer"}
