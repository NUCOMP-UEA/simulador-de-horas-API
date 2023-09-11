from add_hours.application.exceptions.http_exception import HTTPException


class BadRequest(HTTPException):
    status_code = 400


class IncoherentDateBadRequest(BadRequest):
    message = "Date is incoherent"
    code = "badRequest.incoherentDate"


class IncoherentFieldBadRequestDatabase(BadRequest):
    message = "Database field is incoherent"
    code = "badRequest.incoherentFieldDatabase"


class IncoherentRequestBodyBadRequest(BadRequest):
    message = "Request Body is incoherent"
    code = "badRequest.incoherentRequestBody"
