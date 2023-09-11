from add_hours.application.exceptions.http_exception import HTTPException


class UnprocessableEntity(HTTPException):
    status_code = 422


class InvalidIdUnprocessableEntityDatabase(UnprocessableEntity):
    message = "Invalid database id"
    code = "unprocessableEntity.invalidIdDatabase"


class InvalidFileFormatUnprocessableEntity(UnprocessableEntity):
    message = "Invalid file format"
    code = "unprocessableEntity.invalidFileFormat"
