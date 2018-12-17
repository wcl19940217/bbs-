from flask import g

from .views import bp, session
import config
from .models import CmsUser, CMSPermission


# session_id使用的，定义后可以在所有的模板中使用
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CmsUser.query.get(user_id)
        if user:
            g.cms_user = user


# 在权限判断的模板中使用的钩子函数，定义后可以在所有的模板中使用
@bp.context_processor
def cms_context_processor():
    return {"CMSPermission": CMSPermission}