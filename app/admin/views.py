# coding:utf8

'''
    视图模块
    Angela
    2018年3月7日11:41:57
'''

# 在当前目录下导入home 蓝图对象
import os
import uuid
from datetime import datetime
from . import admin
from flask import render_template, redirect, url_for, flash, session, request , abort
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm,RoleForm ,AdminForm # 导入表单
from app.models import Admin, Adminlog, Tag, Oplog, Movie, Preview, User, Comment, Moviecol, Userlog, Auth, Role  # 导入模型
from app import db, app
from functools import wraps  # 定义装饰器
from werkzeug.utils import secure_filename  # 文件安全


#################自定义函数####################

## 登录访问控制
def admin_login_req(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


### 保存文件名称
def change_filename(filename):
    """
    修改文件名称
    """
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.context_processor
def tpl_extra():
    """
    上下应用处理器（全局变量）
    """
    try:
        admin = Admin.query.filter_by(name=session["admin"]).first()
    except:
        admin = None
    data = dict(
        online_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        logo="mtianyan.jpg",
        admin=admin,
    )
    # 之后直接传个admin。取admin face字段即可
    return data



def admin_auth(f):
    """
    权限控制装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session["admin_id"]
        ).first()
        auths = admin.role.auths  # 字符串
        auths = list(map(lambda v: int(v), auths.split(",")))  #转化为列表
        auth_list = Auth.query.all()
        #urls = [v.url for v in auth_list for val in auths if val == v.id]
        urls =[]
        for v in auth_list:
            if v.id in auths:
                urls.append(v.url)
        rule = request.url_rule
        print(urls)
        print(rule)
        """"""
        if str(rule) not in urls:
            abort(404)
        return f(*args, **kwargs)

    return decorated_function


#################自定义函数---结束####################


# 使用蓝图创建路由

@admin.route('/')
@admin_login_req
@admin_auth
def index():
    """
    后台首页系统管理
    """
    return render_template('admin/index.html')  # 后台界面


@admin.route('/login/', methods=["GET", "POST"])
def login():
    """
    后台登录
    """
    form = LoginForm()  # 登录表单
    if form.validate_on_submit():  # 表单提交
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()  # 可以考虑统一放在模型中，查询一条记录

        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误!", "err")  # 信息闪现
            return redirect(url_for("admin.login"))

        # 如果是正确的，就要定义session的会话进行保存。
        session["admin"] = data["account"]
        session["admin_id"] = admin.id

        # admin = Admin.query.filter_by(name=session["admin"]).first()
        # g.logo = "mtianyan.jpg"
        # 后台头像实现的可能解决方法，将当前管理员的头像信息，存在session中。
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr,
        )
        db.session.add(adminlog)
        db.session.commit()

        # return redirect(request.args.get("next") or url_for("admin.index"))
        return redirect(url_for("admin.index"))
    return render_template('admin/login.html', form=form)  # 用户登录界面


@admin.route('/logout/')
def logout():
    """
    后台注销登录
    """
    session.pop('admin', None)
    session.pop("admin_id", None)
    return redirect(url_for('admin.login'))  # 用户退出


@admin.route('/pwd/', methods=["POST", "GET"])
@admin_login_req
@admin_auth
def pwd():
    """
    后台密码修改
    """
    form = PwdForm()
    if form.validate_on_submit():  # 验证密码
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data["new_pwd"])  # 修改密码
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html', form=form)  # 修改密码


@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_add():
    """
    标签添加
    """
    form = TagForm()  # 登录表单
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        # 说明已经有这个标签了
        if tag == 1:
            flash("标签已存在", "err")
            return redirect(url_for("admin.tag_add"))
        # 组合数据
        tag = Tag(
            name=data["name"]
        )
        # 添加
        db.session.add(tag)
        db.session.commit()

        # 操作日志--统一入口
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason="添加标签-%s" % data["name"]
        )
        db.session.add(oplog)
        db.session.commit()

        # 闪现提示信息
        flash("标签添加成功", "ok")

        # 跳转
        redirect(url_for("admin.tag_add"))
    return render_template('admin/tag_add.html', form=form)  # 标签添加


@admin.route('/tag/list/<int:page>/')  # 传入整型页码 <int:page>
@admin_login_req
@admin_auth
def tag_list(page=None):
    """
    标签列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/tag_list.html', page_data=page_data)  # 标签列表


@admin.route('/tag/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def tag_edit(id):
    """
    标签编辑
    """
    form = TagForm()
    tag = Tag.query.get_or_404(id)  # 查询是否存在标签
    if form.validate_on_submit():
        data = form.data
        name = data['name']
        tag_count = Tag.query.filter_by(name=name).count()  # 修改后名称是否与数据库中是否存在同名
        if tag.name != data["name"] and tag_count == 1:
            flash("标签已存在", "err")
            return redirect(url_for("admin.tag_edit", id=tag.id))

        # 组合数据
        tag.name = name  # 追加覆盖新标签
        db.session.add(tag)
        db.session.commit()
        flash("标签[{0}]-[{1}] 修改成功".format(tag.id, tag.name), "ok")  # 提示信息
        redirect(url_for("admin.tag_edit", id=tag.id))

    return render_template('admin/tag_edit.html', form=form, tag=tag)  # 编辑标签


@admin.route('/tag/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def tag_del(id):
    """
    标签删除
    """
    tag = Tag.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(tag)
    db.session.commit()
    flash("标签[{0}]删除成功".format(tag.name), "ok")
    return redirect(url_for("admin.tag_list", page=1))


@admin.route('/movie/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def movie_add():
    """
    添加电影
    """
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data  # 获取数据

        # 判断片名是否存在
        movie = Movie.query.filter_by(title=data["title"]).count()
        # 说明已经有这个标签了
        if movie == 1:
            flash("片名已存在", "err")
            return redirect(url_for("admin.movie_add"))

        # 检测文件安全
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)

        # 检测路径，否则创建
        if not os.path.exists(app.config["UP_DIR"]):
            # 创建一个多级目录
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")  # 授权读写

        # 处理文件
        url = change_filename(file_url)
        logo = change_filename(file_logo)

        # 保存文件
        form.url.data.save(app.config["UP_DIR"] + url)  # 拼接字符串
        form.logo.data.save(app.config["UP_DIR"] + logo)

        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            length=data['length'],
            release_time=data['release_time']
        )

        db.session.add(movie)
        db.session.commit()

        flash("添加电影成功！", "ok")
        return redirect(url_for('admin.movie_add'))

    return render_template('admin/movie_add.html', form=form)  # 电影添加


@admin.route('/movie/list/<int:page>/')
@admin_login_req
@admin_auth
def movie_list(page):
    """
    电影列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template('admin/movie_list.html', page_data=page_data)  # 电影添加


@admin.route('/movie/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def movie_edit(id):
    """
    电影编辑
    """

    form = MovieForm()
    # 因为是编辑，所以非空验证空
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))  # 查询是否存在电影
    url = movie.url
    logo = movie.logo
    # 编辑时赋初值，文本域，下拉框
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star

    # 提交操作
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()

        # 检测片名是否已存在
        if movie_count == 1 and movie.title != data["title"]:
            flash("片名已经存在！", "err")
            return redirect(url_for('admin.movie_edit', id=id))

        # 组合数据
        movie.title = data["title"]
        movie.star = data["star"]
        movie.tag_id = int(data['tag_id']),
        movie.area = data['area'],
        movie.length = data['length'],
        movie.release_time = data['release_time']

        # 检测目录
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        # print(data)
        # 检测是否有重新上传电影
        if form.url.data:
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
            os.remove(os.path.join(app.config["UP_DIR"], url))

        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)
            os.remove(os.path.join(app.config["UP_DIR"], logo))

        # 修改数据
        db.session.add(movie)
        db.session.commit()
        flash("电影[{0}]-[{1}] 修改成功".format(movie.id, movie.title), "ok")  # 提示信息
        redirect(url_for("admin.movie_edit", id=movie.id))

    return render_template('admin/movie_edit.html', form=form, movie=movie)  # 编辑标签


@admin.route('/movie/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def movie_del(id):
    """
    电影删除（关联电影统统删除，建议使用下线操作）
    """
    movie = Movie.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(movie)
    db.session.commit()
    flash("电影[{0}]删除成功".format(movie.name), "ok")
    return redirect(url_for("admin.movie_list", page=1))


@admin.route('/preview/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_add():
    Form = PreviewForm()
    if Form.validate_on_submit():
        data = Form.data
        # 判断片名是否存在
        preview_count = Preview.query.filter_by(title=data["title"]).count()
        # 说明已经有这个标签了
        if preview_count == 1:
            flash("预告已存在", "err")
            return redirect(url_for("admin.movie_add"))

        # 检测文件安全
        file_logo = secure_filename(Form.logo.data.filename)

        # 检测路径，否则创建
        if not os.path.exists(app.config["UP_DIR"]):
            # 创建一个多级目录
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")  # 授权读写

        # 处理文件
        logo = change_filename(file_logo)

        # 保存文件
        Form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()

        flash("添加预告成功！", "ok")
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=Form)  # 预告添加


@admin.route('/preview/list/<int:page>/')
@admin_login_req
@admin_auth
def preview_list(page):
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template('admin/preview_list.html', page_data=page_data)  # 预告列表


@admin.route('/preview/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def preview_edit(id):
    """
    预告编辑
    """

    form = PreviewForm()
    # 因为是编辑，所以非空验证空
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))  # 查询是否存在电影
    logo = preview.logo

    # 提交操作
    if form.validate_on_submit():
        data = form.data
        preview_count = preview.query.filter_by(title=data["title"]).count()

        # 检测片名是否已存在
        if preview_count == 1 and preview.title != data["title"]:
            flash("预告已经存在！", "err")
            return redirect(url_for('admin.movie_edit', id=id))

        # 组合数据
        preview.title = data["title"]

        # 检测目录
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        # 检测是否有重新上传

        if form.logo.data:
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
            os.remove(os.path.join(app.config["UP_DIR"], logo))

        # 修改数据
        db.session.add(preview)
        db.session.commit()
        flash("预告[{0}]-[{1}] 修改成功".format(preview.id, preview.title), "ok")  # 提示信息
        redirect(url_for("admin.preview_edit", id=preview.id))

    return render_template('admin/preview_edit.html', form=form, preview=preview)  # 编辑标签


@admin.route('/preview/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def preview_del(id):
    """
    预告删除（建议使用关闭操作）
    """
    preview = Preview.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(preview)
    db.session.commit()
    logo = preview.logo
    os.remove(os.path.join(app.config["UP_DIR"], logo))

    flash("预告[{0}]删除成功".format(preview.title), "ok")
    return redirect(url_for("admin.preview_list", page=1))


@admin.route('/user/view/<int:id>/')
@admin_login_req
@admin_auth
def user_view(id):
    user = User.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    return render_template('admin/user_view.html', user=user)  # 会员查看


@admin.route('/user/list/<int:page>/')
@admin_login_req
@admin_auth
def user_list(page):
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template('admin/user_list.html', page_data=page_data)  # 会员列表


@admin.route('/user/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def user_del(id):
    """
    预告删除（建议使用关闭操作）
    """
    user = User.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(user)
    db.session.commit()

    # 删除文件
    face = user.face
    facename = os.path.join(app.config["UP_DIR"], face)
    if os.path.exists(facename):
        os.remove(facename)

    flash("预告[{0}]删除成功".format(user.name), "ok")
    return redirect(url_for("admin.user_list", page=1))


@admin.route('/comment/list/<int:page>/')
@admin_login_req
@admin_auth
def comment_list(page):
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/comment_list.html', page_data=page_data)  # 评论列表


@admin.route('/comment/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def comment_del(id):
    """
    评论删除
    """
    comnent = Comment.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(comnent)
    db.session.commit()

    flash("评论[{0}]删除成功".format(comnent.id), "ok")
    return redirect(url_for("admin.comment_list", page=1))


@admin.route('/moviecol/list/<int:page>/')
@admin_login_req
@admin_auth
def moviecol_list(page):
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).join(User).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/moviecol_list.html', page_data=page_data)  # 列表


@admin.route('/moviecol/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def moviecol_del(id):
    """
    收藏删除
    """
    moviecol = Moviecol.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(moviecol)
    db.session.commit()

    flash("收藏[{0}]删除成功".format(moviecol.id), "ok")
    return redirect(url_for("admin.moviecol_list", page=1))



@admin.route('/oplog/list/<int:page>/')
@admin_login_req
@admin_auth
def oplog_list(page):
    """
    操作日志列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(
        Oplog.admin_id == Admin.id
    ).order_by(
        Oplog.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/oplog_list.html', page_data=page_data)  # 标签列表


@admin.route('/adminloginlog/list/<int:page>/')
@admin_login_req
@admin_auth
def adminloginlog_list(page):
    """
    管理员列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Adminlog.query.join(Admin).filter(
        Adminlog.admin_id == Admin.id
    ).order_by(
        Adminlog.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/adminloginlog_list.html', page_data=page_data)  # 管理员登录日志


@admin.route('/userloginlog/list/<int:page>/')
@admin_login_req
@admin_auth
def userloginlog_list(page):
    """
    会员登录列表
   """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(
        Userlog.user_id == User.id
    ).order_by(
        Userlog.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/userloginlog_list.html', page_data=page_data)  # 会员登录日志


@admin.route('/auth/list/<int:page>/')
@admin_login_req
@admin_auth
def auth_list(page):
    """
    标签列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/auth_list.html', page_data=page_data)  # 权限管理


@admin.route('/auth/add/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()

    if form.validate_on_submit():
        data = form.data

        # 组合数据
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        try:
            # 执行添加
            db.session.add(auth)
            db.session.commit()
            flash("添加权限成功！", "ok")
        except:
            db.session.rollback()
            flash('添加权限失败，请重新输入！', 'err')

    return render_template('admin/auth_add.html', form=form)  # 权限添加


@admin.route('/auth/del/<int:id>', methods=["GET"])
@admin_login_req
@admin_auth
def auth_del(id):
    """
    权限删除
    """
    auth = Auth.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(auth)
    db.session.commit()

    flash("权限[{0}]删除成功".format(auth.id), "ok")
    return redirect(url_for("admin.auth_list", page=1))


@admin.route('/auth/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req

def auth_edit(id):
    """
    权限编辑
    """
    form = AuthForm()
    auth = Auth.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        try:
            auth.name = data['name']
            auth.url = data['url']
            db.session.add(auth)
            db.session.commit()
            flash("权限[{0}]修改成功".format(auth.id), "ok")
        except:
            db.session.rollback()
            flash("权限[{0}]修改失败".format(auth.id), "err")
    return render_template('admin/auth_edit.html', form=form,auth=auth)  # 权限添加



@admin.route('/role/list/<int:page>/')
@admin_login_req
@admin_auth
def role_list(page):
    """
    角色列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('admin/role_list.html', page_data=page_data)  # 权限管理

@admin.route('/role/add/',methods=["GET","POST"])
@admin_login_req
@admin_auth
def role_add():

    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        auths = request.form.getlist('auths')
        print(data['auths'])
        try:
            role = Role(
                name=data['name'],
                auths=",".join(map(lambda v: str(v), auths))
            )
            db.session.add(role)
            db.session.commit()
            flash("添加[{0}]权限成功".format(data['name']), "ok")
        except:
            db.session.rollback()
            flash("添加[{0}]权限失败".format(data['name']), "err")

    return render_template('admin/role_add.html',form=form)  # 角色添加

@admin.route('/role/del/<int:id>/', methods=["GET"])
@admin_login_req
@admin_auth
def role_del(id):
    """
    角色删除
    """
    role = Role.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(role)
    db.session.commit()

    flash("角色[{0}]删除成功".format(role.id), "ok")
    return redirect(url_for("admin.role_list", page=1))


@admin.route('/role/edit/<int:id>/', methods=["GET", "POST"])
@admin_login_req
@admin_auth
def role_edit(id):
    """
    角色编辑
    """
    form = RoleForm()
    role = Role.query.get_or_404(int(id))
    if request.method == "GET":
        auths = role.auths
        if auths :
            # get时进行赋值。应对无法模板中赋初值
            form.auths.data = list(map(lambda v: int(v), auths.split(",")))
    if form.validate_on_submit():
        data = form.data
        try:
            role.name = data['name']
            auths = request.form.getlist('auths')
            role.auths = ",".join(map(lambda v: str(v), auths))
            db.session.add(role)
            db.session.commit()
            flash("权限[{0}]修改成功".format(role.id), "ok")
        except:
            db.session.rollback()
            flash("权限[{0}]修改失败".format(role.id), "err")
    return render_template('admin/role_edit.html', form=form,role=role)




@admin.route("/admin/add/", methods=["GET", "POST"])
@admin_login_req
@admin_auth
def admin_add():
    """
    添加管理员
    """
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            role_id=data["role_id"],
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功！", "ok")
    return render_template("admin/admin_add.html", form=form)


@admin.route("/admin/list/<int:page>/", methods=["GET"])
@admin_login_req
@admin_auth
def admin_list(page=None):
    """
    管理员列表
    """
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/admin_list.html", page_data=page_data)