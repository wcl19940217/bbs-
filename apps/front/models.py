import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime


from exts import db


class GenderEnum(object):
    MALE = 1
    FEMALE = 2
    SECURE = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(50), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(100))
    avator = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    # gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    gender = db.Column(db.Integer, default=GenderEnum.UNKNOW)
    last_login_time = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    join_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password') # 调用新的方法
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args, **kwargs) # 其他的交给父类处理

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)
