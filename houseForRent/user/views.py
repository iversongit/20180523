from flask import Blueprint, render_template, request, jsonify, session
from user.models import User
from utils.functions import db
from utils import status_code
import re
import os
from utils.functions import is_login

from utils.settings import UPLOAD_DIRS

user = Blueprint("user",__name__)

@user.route("/")
def index():
    return "这里是首页"

@user.route("/createdb/")
@is_login
def create_db():
    db.create_all()
    return "数据库创建成功"

@user.route("/dropdb/")
@is_login
def drop_db():
    db.drop_all()
    return "数据库删除成功"

# 注册页面
@user.route('/register/',methods=['GET'])
def register():
    return render_template("register.html")

# 注册请求
@user.route('/register/',methods=['POST'])
def user_register():
    register_dict = request.form
    mobile = register_dict.get("mobile")
    password = register_dict.get("password")
    password2 = register_dict.get("password2")

    # 判断三个字段是否为空，为空则报错
    if not all([mobile,password,password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)

    # 判断手机号(初始用户名)是否合法
    if not re.match(r"^1[345789]\d{9}$",mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    # 判断两次输入密码是否一致：
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    # 判断用户名是否已经存在,如果计数大于等于1，则该用户已存在
    if User.query.filter(User.phone == mobile).count():
        return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXISTS)

    # 上述判断都通过，则创建新用户
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password # 已经在修改器中为密码加了密
    try:
        user.add_update() # 添加并提交新建用户
        return jsonify(status_code.SUCCESS) # 提交不成功，返回SUCCESS
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)  # 提交不成功，返回数据库错误

    # register_dict = request.form
    # mobile = register_dict.get('mobile')
    # password = register_dict.get('password')
    # password2 = register_dict.get('password2')
    #
    # if not all([mobile,password,password2]): # 三个字段不为空
    #     return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)
    #
    # # 验证手机号，用正则表达式
    # if not re.match(r'^1[345789]\d{9}$',mobile):
    #     return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    #
    # # 验证两个密码
    # if password != password2:
    #     return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)
    #
    # # 验证用户是否已经存在
    # if User.query.filter(User.phone==mobile).count(): # False:未注册  True:已注册
    #     return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXISTS)
    #
    #
    # user = User()
    # user.phone = mobile
    # user.name = mobile
    # user.password = password
    # try:
    #     user.add_update()
    #     return jsonify(status_code.SUCCESS)
    # except Exception as e:
    #     return jsonify(status_code.DATABASE_ERROR)

# 登录页面
@user.route('/login/',methods=['GET'])
def login():
    return render_template("login.html")

# 登录请求
@user.route('/login/',methods=['POST'])
def user_login():
    user_dict = request.form
    mobile = user_dict.get("mobile")
    password = user_dict.get("password")
    if not all([mobile,password]):
        return jsonify(status_code.PARAMS_ERROR)

    if not re.match(r'^1[345789]\d{9}$',mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    user = User.query.filter(User.phone==mobile).first()
    if user:
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXISTS)

@user.route('/my/',methods=["GET"])
@is_login
def my():  # 跳转到我的爱家页面
    return render_template("my.html")

@user.route('/user/',methods=["GET"])
@is_login
def get_user_profile():  # 在我的爱家页面显示个人信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify(user=user.to_basic_dict(),code="200")

@user.route('/profile/',methods=["GET"])
@is_login  # 只有登录了才能访问相应的方法
def profile():
    return render_template("profile.html")

@user.route('/user/',methods=["PUT"])
@is_login
def user_profile():  # ctrl + F5 快速清缓存   修改个人信息，头像和名字
    user_dict = request.form
    # username = user_dict.get('username')
    # user = User.query.filter(User.id == session['user_id']).first()
    # if User.query.filter(User.name == username).count():
    #     print(status_code.MODIFY_NAME_IS_EXIST)
    #     return jsonify(status_code.MODIFY_NAME_IS_EXIST)
    #
    # if username:
    #     user.name = username
    #     try:
    #         db.session.commit()
    #         return jsonify(code=status_code.OK)
    #     except Exception as e:
    #         return jsonify(status_code.DATABASE_ERROR)

    file_dict = request.files
    if 'avatar' in file_dict:
        f1 = file_dict['avatar']
        if not re.match(r'^image/.*$',f1.mimetype): # mimetype:上传文件的类型
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)
        # url = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # url = os.path.join(url,'static')
        # url = os.path.join(url,'upload')
        # url = os.path.join(url,f1.filename)
        # f1.save(url) # 保存图片
        url = os.path.join(UPLOAD_DIRS, f1.filename)
        f1.save(url)  # 保存图片到指定路径

        user = User.query.filter(User.id == session['user_id']).first()
        image_url = os.path.join('/static/upload',f1.filename)
        user.avatar = image_url
        try:
            user.add_update()
            return jsonify(code=status_code.OK,url=image_url)
            # return render_template("profile.html",url=image_url)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
    elif 'username' in user_dict:
        username = user_dict.get('username')
        if User.query.filter(User.name == username).count():
            print(status_code.MODIFY_NAME_IS_EXIST)
            return jsonify(status_code.MODIFY_NAME_IS_EXIST)

        user = User.query.get(session['user_id'])
        user.name = username
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except Exception as e:
            return jsonify(status_code.DATABASE_ERROR)
    else:
        return jsonify(status_code.PARAMS_ERROR) # 什么都不传时也会报错

@user.route('/auth/',methods=['GET'])
@is_login
def auth():
    return render_template("auth.html")

@user.route('/auths/',methods=['GET'])
@is_login
def get_user_auth():
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.OK,
                   id_name=user.id_name,
                   id_card=user.id_card)

@user.route('/auths/',methods=['PUT'])
@is_login
def user_auth():
    user_dict = request.form
    real_name = user_dict.get("real_name")
    real_id_card = user_dict.get("real_id_card")

    if not all([real_name,real_id_card]):
        return jsonify(status_code.AUTH_PARAMS_ERROR)

    if not re.match(r'^\d{18}$',real_id_card):
        return jsonify(status_code.AUTH_IDCARD_ERROR)

    try:
        user = User.query.filter(User.id == session['user_id']).first()
        user.id_name = real_name
        user.id_card = real_id_card
        user.add_update()
    # try:
    #     db.session.commit()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)

@user.route('/logout/')
@is_login
def user_logout():
    session.clear()
    return jsonify(status_code.SUCCESS)



