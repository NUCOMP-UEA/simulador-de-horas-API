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
