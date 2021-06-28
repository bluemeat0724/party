from flask import Flask
from flask_cors import CORS
from app.config import config
from flask_sqlalchemy import SQLAlchemy
from app.models import db
from flask_bootstrap import Bootstrap
from app.config import config

import logging
from logging.handlers import RotatingFileHandler

cors= CORS()
bootstrap = Bootstrap()
# db = SQLAlchemy()

def setupLogging(levle):
    # 业务逻辑已开启就加载日志
    # 设置日志的记录等级
    logging.basicConfig(level=levle)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    setupLogging(config[config_name].LOGGIONG_LEVEL)

    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    app.config.from_object(config[config_name])

    # cors.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    from app.apis import api
    app.register_blueprint(api)

    # with app.app_context():
    #     #     db.create_all()


    return app
