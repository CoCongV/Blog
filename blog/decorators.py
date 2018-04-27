from functools import wraps

from sanic.exceptions import Unauthorized, Forbidden

from blog.models import User


def login_requred():
    def decorator(f):
        @wraps(f)
        async def wrapper(request, *args, **kwargs):
            token = request.headers.get('Authorization').split(' ')[1]
            user = await User.verify_auth_token(request.app.config.SECRET_KEY,
                                                token)
            if not user:
                raise Unauthorized('Unauthorized')
            else:
                kwargs['user'] = user
                return f(request, *args, **kwargs)
        return wrapper
    return decorator


def permission_reuired(permission):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, user, **kwargs):
            if not user.can(permission):
                raise Forbidden('permission exception')
            return f(*args, **kwargs)
        return wrapper
    return decorator
