# coding:utf8

import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_redis import FlaskRedis

# 实例化对象
app = Flask(__name__)

# 数据库连接配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@192.168.4.9:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'dbti22qtwawxwsgb418lcg0y8d3q20mv'
app.config["SQLALCHEMY_ECHO"] = True

# 使用绝对路径  ()
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")

#Redis
app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"

# 开启调试模式
app.debug = True

# 实例化对象
db = SQLAlchemy(app)
redis = FlaskRedis(app)

# 导入蓝图模块 # 不要在生成db之前导入注册蓝图。
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')





# 404 错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html")  # 搜索页面
