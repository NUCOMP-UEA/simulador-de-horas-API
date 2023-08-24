from enum import Enum

from pydantic import BaseModel


class CourseEnum(str, Enum):
    computer_engineering = "ECP"
    computing_degree = "LIC"
    information_system = "SI"


class StudentRequest(BaseModel):
    name: str
    enrollment: str
    email: str
    course: CourseEnum

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Lorem Ipsum",
                "enrollment": "2015080001",
                "email": "loremipsum@example.com",
                "course": "ECP",
            }
        }
