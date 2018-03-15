- 规划项目目录结构
- flask 蓝图使用（路由）
- SQLAlchemy [官方文档](http://www.pythondoc.com/flask-sqlalchemy/index.html)
- pip install -i http://pypi.douban.com/simple -- trusted-host pypi.douban.com Flask-SQLAlchemy
- {{url_for('home.index')}}  生成路由
- {{url_for('static',filename='base/images/logo.png')}}  生成静态文件
- Jinja 模板引擎使用 [中文文档](http://docs.jinkan.org/docs/jinja2/)
- 404 页面，项目初始化界面
    ```
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("home/404.html")  # 搜索页面
    ```
- 生成URL
    ```
    url_for('admin.tag_adds') 模块.函数名称
    @admin.route('/tag/add/') 生成路由URL
    def tag_adds():
        return render_template('admin/tag_add.html')  # 标签添加
    ```
- CSRF
    ```
    app.config['SECRET_KEY'] = 'dbti22qtwawxwsgb418lcg0y8d3q20mv'
    {{ form.csrf_token }}
    
    ```
- SQLAlchemy 使用 [sqlalchemy 手册](http://www.pythondoc.com/flask-sqlalchemy/)
- 过滤闪现消息 [消息闪现](http://docs.jinkan.org/docs/flask/patterns/flashing.html)
- SQLAlchemy 分页操作 [分页](http://www.pythondoc.com/flask-sqlalchemy/api.html#id4)
- 使用JinJa 定义宏，使用在分页 [宏](http://docs.jinkan.org/docs/jinja2/templates.html)
- 数据操作记录需要return 
- 文件上传 [文件上传](http://www.pythondoc.com/flask-wtf/form.html)
- SQLAlchemy — 多表查询
    ```
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    
    # 分配
    {% for v in page_data.items %}
    <tr>
        <td>{{ v.id }}</td>
        <td>{{ v.tag.name }}</td>
    </tr>
    {% endfor %}

    ```
- 编辑非空验证
- 对初始值（文本框和下拉框）
- 上下文处理器 (转化为全局变量) [手册](http://docs.jinkan.org/docs/flask/templating.html#id6)
- 列表转字符串
    ```
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
        
        
        
    #复选框
    from wtforms import StringField,SelectMultipleField,widgets
    auths =SelectMultipleField(
        label="权限列表",
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(html_tag='ol',prefix_label=True),
        #widget=widgets.TableWidget(),
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description="权限列表",
        render_kw={
           # "class": "form-control",
        }
    )
    
    ```
- 权限控制
    - 检测当前访问URL是否在指定权限路由之内
    ```
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
            rule = request.url_rule  # 获取当前访问路由
            #print(urls)
            #print(rule)
            """"""
            if str(rule) not in urls:
                abort(404)
            return f(*args, **kwargs)
    
        return decorated_function
    ```

- 表单验证基类
    - from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
- 自定义表单验证
    - https://wtforms.readthedocs.io/en/stable/validators.html#custom-validators

- 内容搜索，提供搜索页面
    - 分页时需要加入关键字
- 影片评论设计
- Ajax 返回jSON 数据
    ```
        data = dict(ok=1)
        import json
        return json.dumps(data)
    ```
- 使用Redis实现消息对列
    - 弹幕https://github.com/MoePlayer/DPlayer
    - Flask-redis
    - 返回JSON数据结构
    ```
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
    ```

- 部署服务
 - 安装python3
 - 安装mysql yum -y install mariadb-server
    - 启动 systemctl start mariadb.service
    - 自启动 systemctl enable mariadb.service
 - pip freeze > requirements.txt
 - pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt
 - 配置反向代理 
    - nohup python manage.py runserver --host 0.0.0.0 --port 9008 & 
    ```
    upstream movie {
       server 192.168.4.9:9008;
    }
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    server
    {
        listen      80;
        server_name	localhost;
        index index.html index.php index.phtml;
        root /usr/share/nginx/html;
    
        # 反向代理
        location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host; 
        proxy_redirect off; 
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Scheme $scheme;
        proxy_http_version 1.1; 
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://movie; 
        }
        
        # 限制访问
        location ~ \.(flv|mp4|avi|mov)$
        {
        limit_conn addr 1;
        limit_rate 200k;
        rewrite ^/static/uploads/(.+?).(flv|mp4|mov|avi)$ /uploads/$1.$2 permanent;
        }
       
        #图片防止盗链
        #location ~* \.(gif|jpg|png|bmp)
        #{
          #valid_referers none blocked 192.168.4.9 *.bluepay.asia server_name ~\.goole\. ~\.baidu\.;
          #if ($invalid_referer){
        #return 403;
            #rewrite ^/ http://www.baidu.com/403.jpg;
          #}			
        #}
        # 错误日志
        access_log /var/log/nginx/access_80.log;
        error_log /var/log/nginx/error_80.log;
    
    
    }

    ```
- 流媒体访问限制
    - 限制单个IP能发起的连接数：limit_conn addr 1; # 并发打开播放数
    - 限制视频速率：limit_rate 1024k  # 清晰度，下载数据
    - 刷新nginx nginx -s reload  
- 资源 https://github.com/mtianyan/movie_project
- 反向代理 https://www.imooc.com/article/19538


    
    