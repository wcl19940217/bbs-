from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from flask import g

from apps.front.forms import BaseForm
from utils import zlcache


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱'), InputRequired(message='请输入登录名邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='输入正确的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次密码不一致')])

    # def get_errors(self):
    #     message = self.errors.popitem()[1][0]
    #     return message


class ResetMailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度的验证码')])

    def validate_captcha(self, field):
        print(field.data)
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache and captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('邮箱和当前使用邮箱一致')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = StringField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id = StringField(validators=[InputRequired(message='请输入轮播图的id')])


class DeleteBannerForm(BaseForm):
    banner_id = StringField(validators=[InputRequired(message='请输入轮播图的id')])


class AddboardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入表单名称')])


class UpdateboardForm(AddboardForm):
    board_id = StringField(validators=[InputRequired(message='请输入板块id')])


class DeleteboardForm(BaseForm):
    board_id = StringField(validators=[InputRequired(message='请输入板块id')])