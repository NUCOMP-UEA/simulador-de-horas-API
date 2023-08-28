import logging
import os

import uvicorn

from dotenv import load_dotenv

from add_hours.infra.motor.database_setup import Database
from add_hours.routes.fastapi_setup import app
from add_hours.utils.init_services import init_services


def start():
    path_env = "./config/.env"
    load_dotenv(path_env)

    Database.connect()

    init_services()

    uvicorn.run(
        app,
        port=int(os.getenv("API_PORT", "8000")),
        host=os.getenv("API_HOST", "localhost"),
        log_level=logging.DEBUG,
    )


if __name__ == "__main__":
    start()
