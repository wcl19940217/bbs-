from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import Regexp, EqualTo, InputRequired, URL, ValidationError
from utils import zlcache


class BaseForm(Form):
    def get_errors(self):
        try:
            message = self.errors.popitem()[1][0]
        except:
            message = ''
        return message

    def validate(self):
        return super(BaseForm, self).validate()


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[3456879]\d{9}', message='请输入正确格式的手机号')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的手机验证码')])
    username = StringField(validators=[Regexp(r'.{2,20}', message='输入正确格式的用户名')])
    # username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='输入正确格式的密码')])
    # password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo('password1', message='两次密码不一致')])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message='请输入正确格式的验证码')])

    def validate_sms_captcha(self, field): #TODO
        sms_captcha = field.data
        telephone = self.telephone.data
    #
        # sms_captcha_mem = zlcache.get(telephone)
        if sms_captcha != '1234':
        # if not sms_captcha_mem and sms_captcha_mem.lower() != sms_captcha.lower():  #todo
            raise ValidationError(message='短信验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data

        graph_captcha_mem = zlcache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            # raise ValidationError(message='图形验证码错误')  #TODO
            pass


class SigninForm(BaseForm):
    # email = StringField(validators=[Email(message='请输入正确的邮箱'), InputRequired(message='请输入登录名邮箱')])
    telephone = StringField(validators=[Regexp(r'1[3465879]\d{9}', message='请输入正确格式的手机号')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='输入正确格式的密码')])
    # password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    content = StringField(validators=[InputRequired(message='请输入内容')])
    board_id = StringField(validators=[InputRequired(message='请输入板块id')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id')])


class SettingForm(BaseForm):
    username = StringField(validators=[InputRequired(message='必须输入用户名')])
    realname= StringField()
    email = StringField()
    avatar = StringField() #TODO
    signature = StringField()
