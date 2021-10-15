from json import load
from flask_jwt_extended import get_current_user

def admin_verify(func):

    def wrapper(*args, **kwargs):

        with open("admins.json", "r") as json_file:
            admins = load(json_file)
            admins_email = [admin['email'] for admin in admins]

            if not get_current_user().email in admins_email:
                return {"error":"Access restricted to authorized users only"}, 403

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper