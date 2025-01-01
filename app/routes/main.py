"""
主路由
"""
from flask import Blueprint, render_template
from app.models.city import City

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """首页路由"""
    # 获取最新添加的15个城市
    cities = City.query.order_by(City.created_at.desc()).limit(15).all()
    return render_template('index.html', cities=cities)
