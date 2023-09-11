from add_hours.application.exceptions.http_exception import HTTPException


class Conflict(HTTPException):
    status_code = 409


class CertificateConflictStorage(Conflict):
    message = "Certificate is already issued"
    code = "conflict.certificateStorage"
