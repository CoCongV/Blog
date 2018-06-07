from sanic.exceptions import SanicException, add_status_code


@add_status_code(409)
class UserAlreadyExistsException(SanicException):

    message = 'USER ALREADY EXISTS'

    def __init__(self, message=None):
        if message:
            self.message = message
