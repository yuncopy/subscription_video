# coding:utf8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField,SelectMultipleField,BooleanField,widgets
from wtforms.validators import DataRequired, ValidationError,EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import Admin, Tag , Auth,Role


# 管理员登录表单
class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空") # 表填提示
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # 注释此处显示forms报错errors信息
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],  # 验证器
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # 注释此处显示forms报错errors信息
            # "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 检测账号
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()  # 查询记录数
        if admin == 0:
            raise ValidationError("账号不存在，请重新输入")   # 抛出异常



# 标签表单
class TagForm(FlaskForm):
    name = StringField(
        label="标签名称",
        validators=[
            DataRequired("标签名不能为空")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )




# 电影表单
class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired("片名不能为空")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label='文件',
        validators=[
            FileRequired("文件不能为空"),
            FileAllowed(['rmvb','mp4','mov','mtv','wmv','avi','3gp','amv','flv'], '上传视频格式有误')
        ],
        description="文件"
    )
    info = TextAreaField(
        label='介绍',
        validators=[
            DataRequired("介绍不能为空")
        ],
        description="介绍",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入介绍！"
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            FileRequired("封面不能为空"),
            FileAllowed(['jpg','jpeg','gif','png','bmp'], '上传图片格式有误')
        ],
        description="封面"
    )
    star =SelectField(
        label='星级',
        validators=[
            DataRequired("请选择星级！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],  # 元组
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    # 标签要在数据库中查询已存在的标签
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        # 通过列表生成器生成列表
        choices=[(v.id, v.name) for v in Tag.query.all()],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("片长不能为空！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("上映时间不能为空！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


#预告表单
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("预告标题不能为空")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    logo = FileField(
        label='预告封面',
        validators=[
            FileRequired("预告封面不能为空"),
            FileAllowed(['jpg', 'jpeg', 'gif', 'png', 'bmp'], '上传图片格式有误')
        ],
        description="预告封面"
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 修改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("旧密码不能为空！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # 验证密码是否正确
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")




# 权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("权限名称不能为空！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称！"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("权限地址不能为空！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址！"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 角色管理
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("角色名称不能为空！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！"
        }
    )
    # 多选框
    """
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        # 动态数据填充选择栏：列表生成器,
        # choices 参数来传入可选择项，每个项是一个(值, 显示名称)对，
        # 同时它们也有一个参数coerce 参数来强制转换选择项"值"的类型，比如 coerce=int。
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description="权限列表",
        render_kw={
            "class": "form-control",
        }
        #传入一个字典（render_kw），把需要添加到字段的属性以键值对的形式
    )
    """
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
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


# 管理员管理
class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("管理员名称不能为空！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称！",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("管理员密码不能为空！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！",
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("管理员重复密码不能为空！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！",
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in Role.query.all()],
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )