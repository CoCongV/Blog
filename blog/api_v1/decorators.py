from functools import wraps
from flask import g
from werkzeug.exceptions import Forbidden


def permission_required(permission, exc=Forbidden):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                raise exc()
            return f(*args, **kwargs)
        return decorated_function
    return decorator
