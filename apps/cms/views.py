# 系统库
from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from flask_mail import Message
import string, random
from flask_paginate import Pagination, get_page_parameter


# 自己写的模块
from .forms import LoginForm, ResetPwdForm, ResetMailForm, AddBannerForm, UpdateBannerForm, DeleteBannerForm, AddboardForm, \
    UpdateboardForm, DeleteboardForm
from .models import CmsUser, CMSPermission, CMSRole
from .decorators import login_required, permission_required
import config
from exts import db, mail
from utils import restful, zlcache
from ..models import BannerModel, AddBoardModel, PostModel, HighlightPostModel, CommonModel
from apps.front.models import FrontUser
# from apps.hooks import request_count_total

bp = Blueprint('cms', __name__, url_prefix='/cms')


# 首页
@bp.route('/')
@login_required
# @request_count_total
def index():
    return render_template('cms/cms_index.html')


# 登出
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 个人中心
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 发送邮件的接口
@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.paramerror(message='请传递参数')

    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(10)))
    # source.extend([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    captcha = "".join(random.sample(source, 6))
    message = Message('flask论坛验证码发送', recipients=[email], body='验证码是{}'.format(captcha))
    try:
        mail.send(message)

    except:
        return restful.servererror()
    zlcache.set(email, captcha)
    return restful.success()


# 发送邮件
@bp.route('/email/')
def send_email():
    message = Message('flask论坛验证码发送', recipients=['18804928235@163.com'], body='测试')
    mail.send(message)
    return 'success'


# 评论模板
@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    comments = None
    total = 0
    query_obj = CommonModel.query.order_by(CommonModel.create_time.desc())
    comments = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    content = {
        'comment_list': comments,
        'pagination': pagination
    }
    return render_template('cms/cms_comments.html', **content)


# 删除评论
@bp.route('/dcomments/', methods=["POST"])
@login_required
@permission_required(CMSPermission.COMMENTER)
def dcomments():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.paramerror(message='请传入评论id')
    comment = CommonModel.query.get(comment_id)
    if not comment:
        return restful.paramerror('没有这篇评论')
    db.session.delete(comment)
    db.session.commit()
    return restful.success()


# 帖子
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    posts = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    context = {
        'post_list': posts,
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html', **context)


# 精华帖子
@bp.route('/hpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.paramerror(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramerror('没有这篇帖子')
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


# 取消精华帖子
@bp.route('/uhpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.paramerror(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramerror('没有这篇帖子')
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


# 删除帖子
@bp.route('/dpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.paramerror(message='请传入帖子id')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.paramerror('没有这篇帖子')
    db.session.delete(post)
    db.session.commit()
    return restful.success()


#  板块管理
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    # posts = None
    total = 0
    query_obj = AddBoardModel.query.order_by(AddBoardModel.create_time.desc())
    boards_models = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    # boards_models = AddBoardModel.query.all()
    return render_template('cms/cms_boards.html', boards_models=boards_models, pagination=pagination)


# 添加板块
@bp.route('/aboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddboardForm(request.form)
    if form.validate():
        name = form.name.data
        board = AddBoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramerror()


# 更新板块
@bp.route('/uboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateboardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = AddBoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个板块')
    else:
        return restful.paramerror(form.get_errors())


# 删除板块
@bp.route('/dboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    form = DeleteboardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board = AddBoardModel.query.get(board_id)
        if board:
            db.session.delete(board)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个板块')
    else:
        return restful.paramerror(form.get_errors())


# 前台用户管理
@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    # posts = None
    total = 0
    query_obj = FrontUser.query.order_by(FrontUser.join_time.desc())
    front_users = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    # front_users = FrontUser.query.all()
    return render_template('cms/cms_fusers.html', front_users=front_users, pagination=pagination)


# cms用户
@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    # posts = None
    total = 0
    query_obj = CmsUser.query.order_by(CmsUser.join_time.desc())
    cms_users = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    # cms_users = CmsUser.query.all()
    return render_template('cms/cms_cusers.html', cms_users=cms_users)


# cms组
@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    cms_role = CMSRole.query.all()
    return render_template('cms/cms_croles.html', cms_role=cms_role)


# 轮播图
@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


# 插入轮播图
@bp.route('/abanner/', methods=["POST"])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramerror(form.get_errors())


# 编辑轮播图
@bp.route('/ubanner/', methods=["POST"])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个轮播图')
    else:
        return restful.paramerror(form.get_errors())


# 删除轮播图
@bp.route('/dbanner/', methods=["POST"])
@login_required
def dbanner():
    form = DeleteBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            db.session.delete(banner)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个轮播图')
    else:
        return restful.paramerror(form.get_errors())

    # banner_id = request.form.get('banner_id')
    # if not banner_id:
    #     return restful.params_error(message='请传入轮播图id！')
    #
    # banner = BannerModel.query.get(banner_id)
    # if not banner:
    #     return restful.params_error(message='没有这个轮播图！')
    #
    # db.session.delete(banner)
    # db.session.commit()
    # return restful.success()


# 登录
class LoginView(views.MethodView):
    # decorators = [request_count_total]

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CmsUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    #如果设置session。过期时间是31天 ,如果需要自己制定时间，写在配置文件里面，会自动寻找，否则就是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                message = form.get_errors()
                return self.get(message=message)
        else:
            message = form.get_errors()
            return self.get(message=message)


class ResetPwdView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            newpwd = form.oldpwd.data
            oldpwd = form.oldpwd.data
            user = g.cms_user   # cms_user是数据库表的名字
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()

            else:
                message = form.get_errors()
                if message == '':
                    message = '旧密码错误'
                return restful.paramerror(message=message)
        else:
            message = form.get_errors()
            return restful.paramerror(message=message)


# 修改邮箱
class ResetEmailView(views.MethodView):

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetMailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(form.get_errors())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))

# wiki
# parems()
# methos/post/get
