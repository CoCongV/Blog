from sanic.exceptions import SanicException, add_status_code
from sanic.exceptions import NotFound


@add_status_code(409)
class UserAlreadyExistsException(SanicException):

    message = 'USER ALREADY EXISTS'

    def __init__(self, message=None):
        if message:
            self.message = message


class NotFoundException(NotFound):

    message = 'Not Found'

    def __init__(self, message=None):
        if message:
            self.message = message
