from add_hours.application.exceptions.http_exception import HTTPException


class Unauthorized(HTTPException):
    status_code = 401


class InvalidCredentials(Unauthorized):
    message = "Invalid credentials"
    code = "unauthorized.invalidCredentials"


class InvalidUser(Unauthorized):
    message = "Unauthorized user"
    code = "unauthorized.invalidUser"
