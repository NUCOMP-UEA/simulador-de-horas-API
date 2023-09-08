from abc import ABC, abstractmethod

from add_hours.domain.models.activity.activity import Activity
from add_hours.domain.models.activity.activity_type import ActivityType


class IActivityRepository(ABC):
    @classmethod
    @abstractmethod
    async def save_activity(cls, activity: Activity):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def category_limit_verifier(
        cls, activity: Activity, activity_type: ActivityType
    ):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_activities(
        cls, student_id: str, current_page: int, page_size: int
    ):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def activity_exists(cls, activity_id: str):
        raise NotImplementedError()
