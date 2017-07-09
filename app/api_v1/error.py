from flask_restful import HTTPException

from . import HTTPStatusCode


class PermissionForbiddenError(HTTPException, HTTPStatusCode):
    def __init__(self, description="Permission Forbidden", response=None):
        super(PermissionForbiddenError, self).__init__(description, response)
        self.code = self.PERMISSION_FORBIDDEN
        self.description = description

    def __str__(self):
        return self.__class__.__name__


class UserAlreadyExistsError(HTTPException, HTTPStatusCode):

    def __init__(self, description='A user with that username or email already exists', response=None):
        super(UserAlreadyExistsError, self).__init__(description, response)
        self.code = self.USER_EXIST
        self.description = description

    def __str__(self):
        return self.__class__.__name__ + ' code: %d' % self.code


class AuthorizedError(HTTPException, HTTPStatusCode):

    def __init__(self, description="Auth Fail", response=None):
        super(AuthorizedError, self).__init__(description, response)
        self.code = self.UNAUTHORIZED_ACCESS
        self.description = description
