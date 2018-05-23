from flask import Flask

from house.views import house
from order.views import order_blueprint
from utils.settings import templates_dir,static_dir
from user.views import user
from utils.functions import init_ext
def create_app(config):
    app = Flask(__name__,
                template_folder= templates_dir,
                static_folder=static_dir)

    app.register_blueprint(blueprint=user,url_prefix="/user")
    app.register_blueprint(blueprint=house, url_prefix="/house")
    app.register_blueprint(blueprint=order_blueprint, url_prefix="/order")
    # 数据库相关配置信息的设定
    app.config.from_object(config)  # 自动以键值对的方式加载配置信息
    # 附:from_object源码
    # def from_object:
    #     if isinstance(obj, string_types):
    #         obj = import_string(obj)
    #
    # for key in dir(obj):
    #     if key.isupper():
    #         self[key] = getattr(obj, key)
    # 大写字母的属性它才会进行引入，它引入的方法就是调用通过python标准的api getattr()
    # 函数，将Myobj的属性改成大写后读取Myobj的NAME属性并获取其值正常
    init_ext(app) # 放置所有的app初始化内容
    return app
