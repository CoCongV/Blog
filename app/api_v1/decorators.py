from functools import wraps
from flask import g

from .error import PermissionForbiddenError


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return PermissionForbiddenError()
            return f(*args, **kwargs)
        return decorated_function
    return decorator
