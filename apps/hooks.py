from functools import wraps
from .models import RequestCount
from exts import db
from flask import session

# todo
# def request_count_total(func):
#     @wraps(func)
#     def _inner(*args, **kwargs):
#         request_counts = RequestCount()
#         if request_counts.cms_login_counts == None:
#             request_counts.cms_login_counts = 1
#         else:
#             request_counts.cms_login_counts += 1
#         db.session.add(request_counts)
#         db.session.commit()
#
#         return func(*args, **kwargs)
#     return _inner


