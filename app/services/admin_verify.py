from flask_jwt_extended import get_current_user

def admin_verify(func):

    def wrapper(*args, **kwargs):
        if not get_current_user().admin:
            return {"error":"Access restricted to authorized users only"}, 403

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper
