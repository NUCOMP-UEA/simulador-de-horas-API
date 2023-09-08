import asyncio
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

    init_services()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Database.connect())

    config = uvicorn.Config(
        app=app, loop="auto", log_level=logging.DEBUG,
        port=int(os.getenv("API_PORT", "8000")),
        host=os.getenv("API_HOST", "localhost")
    )
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    start()
