from add_hours.application.exceptions.http_exception import HTTPException


class NotFound(HTTPException):
    status_code = 404


class ActivityNotFoundInDatabase(NotFound):
    message = "Activity is not registered in database"
    code = "notFound.activityDatabase"


class ActivityTypeNotFoundInDatabase(NotFound):
    message = "Activity category is not registered in database"
    code = "notFound.activityTypeDatabase"


class StudentNotFoundInDatabase(NotFound):
    message = "Student is not registered in database"
    code = "notFound.studentDatabase"
