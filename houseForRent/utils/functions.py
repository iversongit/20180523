from flask import session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # 实例化数据库
se = Session()
def get_db_url(DATABASE):
    user = DATABASE.get('USER')[0] if isinstance(DATABASE.get('USER'),tuple) else DATABASE.get('USER')
    password = DATABASE.get('PASSWORD')[0] if isinstance(DATABASE.get('PASSWORD'),tuple) else DATABASE.get('PASSWORD')
    host = DATABASE.get('HOST')[0] if isinstance(DATABASE.get('HOST'),tuple) else DATABASE.get('HOST')
    name = DATABASE.get('NAME')[0] if isinstance(DATABASE.get('NAME'),tuple) else DATABASE.get('NAME')
    port = DATABASE.get('PORT')[0] if isinstance(DATABASE.get('PORT'),tuple) else DATABASE.get('PORT')
    db = DATABASE['DB'][0] if isinstance(DATABASE.get('DB'),tuple) else DATABASE.get('DB')
    driver = DATABASE.get('DRIVER')[0] if isinstance(DATABASE.get('DRIVER'),tuple) else DATABASE.get('DRIVER')
    # print(db)
    # print(driver)
    # print(user)
    # print(password)
    # print(host)
    # print(port)
    # print(name)


    # print('{}+{}://{}:{}@{}:{}/{}'.format(db,driver,user,password,host,port,name))
    return '{}+{}://{}:{}@{}:{}/{}'.format(db,driver,user,password,host,port,name)

def init_ext(app):
    db.init_app(app=app)
    se.init_app(app=app)

import functools
def is_login(view_func): # view_func：被装饰的函数
    @functools.wraps(view_func)
    def decorator(): # decorator:名称可以随便写
        try:
            # 验证用户是否登录，判断session中是否有user_id
            # 没有则会报异常
            # if session['user_id']:
            if 'user_id' in session:
                return view_func()
            else:
                return redirect("/user/login/")
        except:
            return redirect("/user/login/")
    return decorator


