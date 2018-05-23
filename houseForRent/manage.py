from flask_script import Manager
from utils.app import create_app
from utils.config import Config

app = create_app(Config) # Config(类) 装载配置信息
manager = Manager(app=app)


if __name__ == '__main__':
    manager.run()
