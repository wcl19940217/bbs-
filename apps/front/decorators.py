from functools import wraps
import config
from flask import redirect, session, url_for


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner

