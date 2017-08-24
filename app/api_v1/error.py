from flask_restful import HTTPException

from . import HTTPStatusCodeMixin


class PermissionForbiddenError(HTTPException, HTTPStatusCodeMixin):
    """
    Permission Exception
    """

    def __init__(self, description="Permission Exception", response=None):
        super(PermissionForbiddenError, self).__init__(description, response)
        self.code = self.PERMISSION_FORBIDDEN
        self.description = description

    def __str__(self):
        return self.__class__.__name__


class UserAlreadyExistsError(HTTPException, HTTPStatusCodeMixin):
    """
    User Info Already Exists
    """

    def __init__(self, description='User Info Already Exists', response=None):
        super(UserAlreadyExistsError, self).__init__(description, response)
        self.code = self.USER_EXIST
        self.description = description

    def __str__(self):
        return self.__class__.__name__ + ' code: %d' % self.code


class AuthorizedError(HTTPException, HTTPStatusCodeMixin):
    """
    Authentication Failed
    """

    def __init__(self, description="Authentication Fail", response=None):
        super(AuthorizedError, self).__init__(description, response)
        self.code = self.UNAUTHORIZED_ACCESS
        self.description = description

    def __str__(self):
        return self.__class__.__name__ + '{}'.format(self.description)


class FileError(HTTPException, HTTPStatusCodeMixin):
    """
    file not exist
    """

    def __init__(self, description="File Not Exist", response=None):
        super().__init__(description, response)
        self.code = self.NOT_FOUND
        self.description = description

    def __str__(self):
        return self.__class__.__name__ + '{}'.format(self.description)
