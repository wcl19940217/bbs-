from flask_script import Manager
# from app import app
from exts import db
from flask_migrate import Migrate, MigrateCommand
from apps.cms.models import CmsUser
from apps.cms import models as cms_models # 定义别名
from apps.front import models as front_models
from apps import models as banner_models
from apps.models import AddBoardModel, PostModel, CommonModel
from cmsapp import create_app


CMSUser = cms_models.CmsUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission
FrontUser = front_models.FrontUser

app = create_app()

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('添加成功')


@manager.command
def create_role():
    # 1、访问者
    visitor = CMSRole(name='访问者', desc='只能看相关数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR
    # 2、运营人员
    operator = CMSRole(name='运营人员', desc='管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER
    # 3、管理员
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|\
                        CMSPermission.FRONTUSER|CMSPermission.BOARDER
    # 4、开发者
    developer = CMSRole(name='开发人员', desc='开发人员权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CmsUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('添加成功')
        else:
            print('没有这个角色{}'.format(role))
    else:
        print('{}邮箱没有这个用户'.format(email))


@manager.command
def test_permissions():
    user = CmsUser.query.first()
    if user.has_permissions(CMSPermission.VISITOR):
        print('有此权限')
    else:
        print('没有此项权限')


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()


@manager.command
def create_test_post():
    for x in range(1, 255):
        title = '标题{}'.format(x)
        content = '内容{}'.format(x)
        author = front_models.FrontUser.query.first()
        board = AddBoardModel.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('帖子添加成功')


@manager.command
def create_test_commom():
    for x in range(1, 255):
        content = '评论内容{}'.format(x)
        author = front_models.FrontUser.query.first()
        post = PostModel.query.first()
        author_id = author.id
        post_id = post.id
        common = CommonModel(content=content)
        common.post_id = post_id
        common.author_id = author_id
        db.session.add(common)
        db.session.commit()
    print('帖子添加成功')


if __name__ == '__main__':
    manager.run()
