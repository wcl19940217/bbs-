from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, abort
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func
from datetime import datetime

from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm, SettingForm
from utils import restful, safeutils
from .models import FrontUser
from exts import db
import config
from ..models import BannerModel, AddBoardModel, PostModel, CommonModel, HighlightPostModel
from .decorators import login_required
# from apps.hooks import request_count_total
from apps.models import RequestCount

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # request_count = RequestCount()   #todo
    #
    # if request_count.front_index_counts == None:
    #     request_count.front_index_counts = 1
    # else:
    #     request_count.front_index_counts += 1
    # db.session.add(request_count)
    # db.session.commit()

    board_id = request.args.get('bd', type=int, default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    boards_models = AddBoardModel.query.all()
    # posts = PostModel.query.all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    posts = None
    total = 0
    query_obj = None
    sort = request.args.get('st', type=int, default=1)
    if sort == 2:
        # 按照精华帖排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞数量排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
        # print(query_obj)
        # print(type(query_obj))
    elif sort == 4:
        # 按照评论数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommonModel).group_by(PostModel.id).order_by(func.count(CommonModel.id).desc(),PostModel.create_time.desc())
    else:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
        # posts = PostModel.query.filter_by(board_id=board_id).slice(start, end)
        # total = PostModel.query.filter_by(board_id=board_id).count()
    else:
        # posts = PostModel.query.slice(start, end)
        # total = PostModel.query.count()
        posts = query_obj.slice(start, end)
        total = query_obj.count()

    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=1)
    content = {
        'posts': posts,
        'boards_models': boards_models,
        'banners': banners,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **content) # todo


@bp.route('/test/')
def test():
    return render_template('front/front_index.html')


# 前台帖子发布
@bp.route('/apost/', methods=["POST", "GET"])
@login_required
def apost():
    if request.method == "GET":
        boards_models = AddBoardModel.query.all()
        return render_template('front/front_apost.html', boards_models=boards_models)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = AddBoardModel.query.get(board_id)
            if not board:
                return restful.paramerror(message='没有这个板块')
            post = PostModel(title=title, content=content)
            post.author = g.front_user
            post.board = board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(form.get_errors())


# 帖子详情
@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    id = post_id
    comment_nums = CommonModel.query.filter(CommonModel.post_id == id).count()
    post.comment_nums = comment_nums

    if post.read_nums == None:
        post.read_nums = 1
    else:
        post.read_nums += 1
    db.session.add(post)
    db.session.commit()
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post, comment_nums=comment_nums)


# 前台帖子评论
@bp.route('/acomment/', methods=["POST", "GET"])
@login_required
def acomment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommonModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message='没有这个帖子')
    else:
        return restful.paramerror(form.get_errors())


# 登出
@bp.route('/signout/')
@login_required
def signout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.index'))


# 个人中心
@bp.route('/profile/<user_id>')
@login_required
def profile(user_id=0):
    if not user_id:
        return abort(404)
    user = FrontUser.query.get(user_id)
    if user:
        current_user = user
        return render_template('front/front_profile.html', current_user=current_user)
    else:
        return restful.paramerror(message='此用户不存在')


@bp.route('/profile/posts/', methods=['GET'])
def profile_posts():
    user_id = request.args.get('user_id')
    if not user_id:
        return abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user,
        }
        return render_template('front/front_profile_posts.html', **context)
    else:
        return abort(404)


# 个人中心设置页面
@bp.route('/settings/', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('front/front_settings.html')
    else:
        form = SettingForm(request.form)
        if form.validate():
            username = form.username.data
            realname = form.realname.data
            email = form.email.data
            avatar = form.avatar.data
            signature = form.signature.data

            user_model = g.front_user
            user_model.username = username
            if realname:
                user_model.realname = realname
            if email:
                user_model.email = email
            if avatar:
                user_model.avatr = avatar
            if signature:
                user_model.signature = signature
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(message=form.get_errors())


# 前台注册
class SignupView(views.MethodView):

    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            tel = FrontUser.query.filter(FrontUser.telephone == telephone)
            if tel:
                return restful.paramerror(message='账号密码已存在')
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramerror(form.get_errors())


# 前台登录
class SigninView(views.MethodView):

    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                user.last_login_time = datetime.now()
                db.session.add(user)
                db.session.commit()
                if remember:
                    # 如果设置session。过期时间是31天 ,如果需要自己制定时间，写在配置文件里面，会自动寻找，否则就是31天
                    session.permanent = True
                return restful.success()
            else:
                # message = form.get_errors()
                # return self.get(message=message)
                return restful.paramerror(message='手机号或密码错误')
        else:
            # message = form.get_errors()
            # return self.get(message=message)
            return restful.paramerror(message=form.get_errors())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))