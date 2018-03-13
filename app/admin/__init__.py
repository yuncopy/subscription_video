#coding:utf8

'''
Flask蓝图提供了模块化管理程序路由的功能，使程序结构清晰、简单易懂。
项目初始化文件
Angela
2018年3月7日11:41:57
'''

# 从flask中导入蓝图对象
from flask import Blueprint

#定义蓝图
admin = Blueprint('admin',__name__)

#导入视图模块
import app.admin.views
