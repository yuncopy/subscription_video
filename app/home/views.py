# coding:utf8

"""
    视图模块
    Angela
    2018年3月7日11:41:57
"""
import datetime
from functools import wraps
import os
from werkzeug.utils import secure_filename
import urllib.parse
# 在当前目录下导入home 蓝图对象
import uuid
from werkzeug.security import generate_password_hash
from app import db, app,redis
from app.home.forms import RegistForm,LoginForm,UserdetailForm,PwdForm,CommentForm  # 导入表单
from app.models import User,Userlog,Comment,Movie,Preview,Tag,Moviecol
from . import home
from flask import render_template, url_for, redirect, flash, session, request, Response


#======================自定义函数========start==========

def change_filename(filename):
    """
    修改文件名称
    """
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
               str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 检测是否登录服务
def user_login_req(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function




#======================自定义函数========end==========




# 使用蓝图创建路由

@home.route('/<int:page>/',methods=["GET"])
@home.route("/", methods=["GET"])
def index(page=None):
    """
    首页电影列表
    """
    tags = Tag.query.all()
    page_data = Movie.query
    # 标签
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    # 星级
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    # 时间
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=8)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    u = urllib.parse.urlencode(p)  # 必须是字典
    return render_template(
        "home/index.html",
        tags=tags,
        p=p,
        u=u,
        page_data=page_data)


@home.route('/login/',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data=form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if not user.check_pwd(data["pwd"]):
                flash("密码错误！", "err")
                return redirect(url_for("home.login"))
        else:
            flash("账户不存在！", "err")
            return redirect(url_for("home.login"))

        # 保存会话
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )

        # 异常处理
        try:
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for("home.user"))  # 跳转会员中心
        except:
            db.session.rollback()
    return render_template("home/login.html",form=form)  # 登录页面


@home.route('/logout/')
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("user", None)
    session.pop("user_id", None)
    flash('已安全退出。','ok')
    return redirect(url_for('home.login'))  # 退出跳转到登录界面


@home.route('/register/',methods=["GET","POST"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        #print(user)
        try:
            db.session.add(user)
            db.session.commit()
            flash('恭喜您！注册成功','ok')
        except:
            db.session.rollback()
    return render_template("home/register.html",form=form)  # 会员注册

@home.route('/user/',methods=["GET","POST"])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session["user_id"]))
    face = user.face
    form.face.validators = []
    if request.method == "GET":
        # 赋初值
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data :
            file_face = secure_filename(form.face.data.filename)
            if not os.path.exists(app.config["FC_DIR"]):
                os.makedirs(app.config["FC_DIR"])
                os.chmod(app.config["FC_DIR"])  # 授权读写
            user.face = change_filename(file_face)
            form.face.data.save(app.config["FC_DIR"] + user.face)
            os.remove(os.path.join(app.config["UP_DIR"], face))

        # 检测是否存在 --- 可以统一处理
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在!", "err")
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在!", "err")
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("手机已经存在!", "err")
            return redirect(url_for("home.user"))

        # 保存
        user.name = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.info = data["info"]
        try:
            db.session.add(user)
            db.session.commit()
            flash("修改成功!", "ok")
        except:
            db.session.rollback()
            flash("修改失败!", "ok")

        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)



@home.route('/pwd/',methods=['GET','POST'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user_data = User.query.filter_by(id=int(session["user_id"])).first()
        if not user_data.check_pwd(data["old_pwd"]):
            flash("旧密码错误！", "err")
            return redirect(url_for('home.pwd'))
        # 组合数据
        user_data.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user_data)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout')) # 跳转退出操作
    return render_template("home/pwd.html",form=form)  # 修改密码


@home.route('/comments/<int:page>/')
@user_login_req
def comments(page):
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == session["user_id"]
    ).order_by(
        Comment.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template("home/comments.html", page_data=page_data)  # 评论界面


@home.route('/loginlog/<int:page>',methods=["GET","POST"])
@user_login_req
def loginlog(page):
    """
      标签列表
      """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(id=int(session["user_id"])).order_by(
        Userlog.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template("home/loginlog.html",page_data=page_data)  # 登录日志


@home.route("/moviecol/add/", methods=["GET"])
@user_login_req
def moviecol_add():
    """
    添加电影收藏
    """
    uid = request.args.get("uid", "")
    mid = request.args.get("mid", "")
    moviecol = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid)
    ).count()
    # 已收藏
    if moviecol == 1:
        data = dict(ok=0)
    # 未收藏进行收藏
    if moviecol == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    import json
    return json.dumps(data)


@home.route('/moviecol/<int:page>')
@user_login_req
def moviecol(page):
    """
    电影收藏
    """
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == session["user_id"]
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=8)
    return render_template("home/moviecol.html", page_data=page_data) #收藏界面



@home.route("/animation/")
def animation():
    """
    首页轮播动画
    """
    data = Preview.query.all()
    num = 0
    for v in data:
        v.num = num
        num = int(num) + 1
    return render_template("home/animation.html", data=data) #首页轮播动画


# @home.route("/search/<int:page>/")
@home.route("/search/<int:page>/")
def search(page=None):
    """
   搜索
   """
    if page is None:
        page = 1

    key = request.args.get("key", "") # 获取参数信息

    # 查询电影条数
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()

    # 搜索查询数据
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template("home/search.html", movie_count=movie_count, key=key, page_data=page_data) #搜索页面


@home.route("/play/<int:id>/<int:page>/", methods=["GET", "POST"])
def play(id=None, page=None):
    """
    播放电影
    """
    # 获取电影
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()

    # 获取所有评论
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    # 提交评论
    form = CommentForm()
    if 'user' in session and form.validate_on_submit():  # 提交时验证
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()

        #评论数
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("添加评论成功！", "ok")
        return redirect(url_for('home.play', id=movie.id, page=1))

    # 放在后面避免添加评论播放量
    movie.playnum = movie.playnum + 1
    db.session.add(movie)
    db.session.commit()
    return render_template("home/play.html", movie=movie, form=form, page_data=page_data) #搜索页面





@home.route("/video/<int:id>/<int:page>/", methods=["GET", "POST"])
def video(id=None, page=None):
    """
    弹幕播放器
    """
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()

    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    movie.playnum = movie.playnum + 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        db.session.add(movie)
        db.session.commit()
        flash("添加评论成功！", "ok")
        return redirect(url_for('home.video', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template("home/video.html", movie=movie, form=form, page_data=page_data)


@home.route("/tm/", methods=["GET", "POST"])
def tm():
    """
    弹幕消息处理
    """
    import json
    if request.method == "GET":
        # 获取弹幕消息队列
        id = request.args.get('id')
        # 存放在redis队列中的键值
        key = "movie" + str(id)
        if redis.llen(key):
            msgs = redis.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)
    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data['type'],
            "ip": request.remote_addr,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 1,
            "data": msg
        }
        resp = json.dumps(res)
        # 将添加的弹幕推入redis的队列中
        redis.lpush("movie" + str(data["player"]), json.dumps(msg))
    return Response(resp, mimetype='application/json')