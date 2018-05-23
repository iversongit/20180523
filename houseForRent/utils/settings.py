import os
from utils.functions import get_db_url

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 页面模板
templates_dir = os.path.join(BASE_DIR,'templates')
# 静态模板
static_dir = os.path.join(BASE_DIR,'static')

# 连接数据库
DATABASE = {
    'USER' : 'root',
    'PASSWORD' : '5201314',
    'PORT' : '3306',
    'HOST' : 'localhost',
    'DB' : 'mysql',
    'DRIVER':'pymysql',
    'NAME' : 'houseforrent'
}

# 连接数据库
SQLALCHEMY_DATABASE_URI = get_db_url(DATABASE)

UPLOAD_DIRS = os.path.join(os.path.join(BASE_DIR,'static'),'upload')