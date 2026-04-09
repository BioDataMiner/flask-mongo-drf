# exceptions.py
class APIException(Exception):
    code = 500
    message = "Internal Server Error"

    def __init__(self, message=None, code=None, payload=None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if code:
            self.code = code
        self.payload = payload or {}


class ValidationError(APIException):
    code = 400
    message = "Validation failed"


class AuthenticationFailed(APIException):
    code = 401
    message = "Authentication failed"


class PermissionDenied(APIException):
    code = 403
    message = "Permission denied"


class NotFound(APIException):
    code = 404
    message = "Resource not found"


class MongoDBConnectionError(APIException):
    code = 500
    message = "MongoDB connection failed"
