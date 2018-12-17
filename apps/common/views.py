from flask import Blueprint, request, make_response, jsonify
from io import BytesIO
import qiniu

from utils import alidayu as telephonecode
from utils import zlcache
from config import Text_model
from utils import restful
from .forms import SMSCaptchaForm
from utils.captcha import Captcha


bp = Blueprint('common', __name__, url_prefix='/c')


@bp.route('/')
def index():
    return 'common index'


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(), text.lower())
    # 自截留
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
# 短信验证码接口
# @bp.route('/sms_captcha/', methods=["POST"])
# def sms_captcha():
#     telephone = request.form.get('telephone')
#     if not telephone:
#         return restful.paramerror(message='请传入手机号码!')
#
#     if telephonecode.send_sms(text=Text_model, mobile=telephone):
#         chaptcha = Text_model[7:11]
#         return restful.success()
#     else:
#         # return restful.paramerror(message='短信验证码发送失败')
#         return restful.success()


@bp.route('/sms_captcha/', methods=["POST"])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        text = Text_model
        captcha = Text_model[7:11]
        if telephonecode.send_sms(text=text, mobile=''): # todo
            zlcache.set(telephone, captcha)

            # return restful.success()
            return restful.paramerror(message='短信验证码系统维护中，验证码为1234')
        else:
            # return restful.paramerror(message='短信验证码发送失败')
            zlcache.set(telephone, captcha) # TODO
            # return restful.success()
            return restful.paramerror(message='短信验证码系统维护中，验证码为1234')
    else:
        return restful.paramerror(message='参数错误')


# 七牛云存储
@bp.route('/uptoken/')
def uptoken():
    access_key = '****'
    secret_key = '***'
    q = qiniu.Auth(access_key, secret_key)

    bucket = '**********'
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})