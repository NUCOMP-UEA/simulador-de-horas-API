import os
from typing import Tuple

from uvicorn.config import logger

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import AnyUrl, BaseModel, ValidationError


class MongoConnectionConfig(BaseModel):
    host: AnyUrl


class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

    @classmethod
    def connect(cls):
        try:
            config_connection = MongoConnectionConfig(
                host=os.getenv("MONGO_DATABASE_URL")
            )
            cls.client = AsyncIOMotorClient(str(config_connection.host))

            cls.database = cls.client[
                config_connection.host.path.removeprefix("/")
            ]

            logger.info(
                "Connection established to database in host %s",
                config_connection.host.host,
            )
        except ValidationError as validation_error:
            logger.exception("Invalid database url", exc_info=validation_error)


class MotorBaseModel(BaseModel):
    async def save(self):
        collection = Database.database[
            self.__class__.__name__.removesuffix("Motor").lower()
        ]

        await collection.insert_one(
            self.model_dump(exclude={"_id", "id_", "id"})
        )

    @classmethod
    async def aggregate(cls, pipeline: list):
        collection = Database.database[
            cls.__name__.removesuffix("Motor").lower()
        ]
        if isinstance(pipeline, list):
            return await collection.aggregate(pipeline).to_list(None)

    async def bulk_update(self, id_field, **kwargs):
        collection = Database.database[
            self.__class__.__name__.removesuffix("Motor").lower()
        ]

        await collection.update_one({"_id": id_field}, {"$set": kwargs})

    @classmethod
    async def delete_one(cls, **kwargs):
        collection = Database.database[
            cls.__name__.removesuffix("Motor").lower()
        ]

        if isinstance(kwargs, dict):
            return await collection.delete_one(kwargs)

    @classmethod
    async def paginate_database(cls, **kwargs) -> Tuple[dict, int]:
        collection = Database.database[
            cls.__name__.removesuffix("Motor").lower()
        ]

        if isinstance(kwargs, dict):
            if "current_page" in kwargs and "page_size" in kwargs:
                return (
                    await collection.find()
                    .skip(
                        (int(kwargs["current_page"]) - 1)
                        * int(kwargs["page_size"])
                    )
                    .limit(int(kwargs["page_size"]))
                    .to_list(100),
                    await collection.count_documents({}),
                )

    @classmethod
    async def find_one(cls, **kwargs) -> dict:
        collection = Database.database[
            cls.__name__.removesuffix("Motor").lower()
        ]

        if isinstance(kwargs, dict):
            return await collection.find_one(filter=kwargs)

    @classmethod
    async def exists(cls, **kwargs) -> bool:
        collection = Database.database[
            cls.__name__.removesuffix("Motor").lower()
        ]

        if isinstance(kwargs, dict):
            return await collection.count_documents(filter=kwargs) > 0
