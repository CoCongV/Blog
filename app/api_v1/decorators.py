from functools import wraps
from flask import g


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user:
                return {"message": "Please Login"}, 403
            if not g.current_user.can(permission):
                return {"message": "Insufficient permission"}, 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
