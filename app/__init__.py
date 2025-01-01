"""
应用初始化
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config.config import config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'warning'

def create_app(config_name='default'):
    """
    创建Flask应用实例
    
    Args:
        config_name: 配置名称，默认为default
        
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    from app.views.auth import auth
    from app.views.city import city
    from app.views.main import main
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(city, url_prefix='/city')
    app.register_blueprint(main)
    
    # 导入用户模型以确保 user_loader 被注册
    from app.models.user import User
    
    return app
