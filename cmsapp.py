from flask import Flask
from flask_wtf import CSRFProtect

from apps.cms.views import bp as cms_bp
from apps.front.views import bp as front_bp
from apps.common.views import bp as common_bp
from apps.ueditor.ueditor import bp as ueditor_bp
import config
from exts import db, mail



#工厂函数，注册app使用
def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app) #数据库绑定
    mail.init_app(app) #邮箱
    CSRFProtect(app) #csrf
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)
    return app
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


app = create_app()
if __name__ == '__main__':
    app.run()

