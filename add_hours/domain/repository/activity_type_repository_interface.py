from abc import ABC, abstractmethod

from add_hours.domain.models.activity.activity_type import ActivityType


class IActivityTypeRepository(ABC):
    @classmethod
    @abstractmethod
    async def save_activity_type(cls, activity_type: ActivityType):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def search_activity_type(cls, search: str) -> list[dict]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def activity_type_exists(cls, activity_type_id: str):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update_activity_type(
        cls, activity_type_id: str, activity_type: ActivityType
    ):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete_activity_type(cls, activity_type_id: str):
        raise NotImplementedError()
