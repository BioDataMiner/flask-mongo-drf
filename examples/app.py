import os
import logging
from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, send_from_directory
from flask_mongo_drf.contrib import init_mongodb

from config.settings import Config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_app():
    # 1. 初始化 Flask
    app = Flask(__name__, static_folder='../static/dist', static_url_path='/')
    app.config.from_object(Config)

    # 2. 插件配置
    CORS(app)

    # 3. 初始化 MongoDB 管理器 (关键步骤)
    try:
        init_mongodb(app)
        logger.info("MongoDB initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB: {e}")
        # 在生产环境下，如果数据库连接失败，通常应该让应用启动失败
        # raise e

    # 4. Swagger 配置
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "BioVista API",
            "description": "flask-mongo-drf的自动化接口文档",
            "contact": {
                "responsibleOrganization": "wangyunkai",
                "email": "yunkaiwang0901@gmail.com",
            },
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # 5. 注册蓝图
    from monitor.app import monitor_bp
    app.register_blueprint(monitor_bp, url_prefix='/api/v1')

    # 6. 静态文件处理 (SPA 路由兼容)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            try:
                return send_from_directory(app.static_folder, 'index.html')
            except:
                return "Frontend build not found.", 404

    return app
