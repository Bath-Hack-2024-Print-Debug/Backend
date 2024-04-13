import functools
import firebase_admin
import firebase_admin.auth
from flask import (
    Blueprint, g, request
)
from flask_json import json_response

creds = firebase_admin.credentials.Certificate("firebase.json")
firebase = firebase_admin.initialize_app(creds)

bp = Blueprint('auth', __name__, url_prefix='/auth')


def verify_token(token):
    try:
        return firebase_admin.auth.verify_id_token(token)["uid"]
    except (
            ValueError,
            firebase_admin.auth.InvalidIdTokenError,
            firebase_admin.auth.ExpiredIdTokenError,
            firebase_admin.auth.RevokedIdTokenError
    ):
        return None
    


def check_account(*, required=True):
    """
    Decorator function to perform login before accessing a route

    Usage looks like ``@login(required=True)``

    :param required: whether login is required (False means optional)
    :return: a decorator
    """
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            """
            This is the decorated route handler
            :param kwargs: kwargs passed to the route handler
            :return: a Response
            """
            if not request.headers["Authorization"]:
                # No authentication even attempted, fail or ignore depending on required
                if required:
                    return json_response(status_=401, error="authentication required")
                else:
                    g.user = None
                    return view(**kwargs)
            if not request.headers["Authorization"].startswith("Bearer "):
                # Authentication header has incorrect format
                return json_response(status_=400, error="incorrect authentication")
            g.user = verify_token(request.headers["Authorization"][7:])

            if g.user is None:
                # Failed to verify authentication JWT
                return json_response(status_=401, error="authentication expired, invalid or forged")

            # All is fine, return original view
            return view(**kwargs)

        return wrapped_view
    return decorator
