"""
应用工厂
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config.config import config

# 创建扩展实例
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'warning'

def create_app(config_name='development'):
    """创建应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # 注册蓝图
    from app.views.auth import auth
    from app.views.city import city
    from app.views.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(city, url_prefix='/city')
    app.register_blueprint(main)  # 主页蓝图不需要 url_prefix
    
    # 导入模型
    from app.models.user import User
    from app.models.city import City
    from app.models.review import CityReview
    
    return app
