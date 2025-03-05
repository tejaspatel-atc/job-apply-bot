from http import HTTPStatus

class LLMException(Exception):
    def __init__(self, status_code: int, message: str, error: str = None):
        self.status_code = status_code
        self.message = message
        self.error = error
        super().__init__(f"{message} (Error: {error})" if error else message)



class StatusCodes:
    OK = HTTPStatus.OK
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
    FORBIDDEN = HTTPStatus.FORBIDDEN
    NOT_FOUND = HTTPStatus.NOT_FOUND
    INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
    SERVICE_UNAVAILABLE = HTTPStatus.SERVICE_UNAVAILABLE
