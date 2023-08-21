from abc import ABC, abstractmethod

from add_hours.domain.models.activity.activity import Activity


class IActivityRepository(ABC):
    @classmethod
    @abstractmethod
    async def save_activity(cls, activity: Activity):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_activities(cls, current_page: int, page_size: int):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def activity_exists(cls, activity_id: str) -> bool:
        raise NotImplementedError()
