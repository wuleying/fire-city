"""
主页视图
"""
from flask import Blueprint, render_template
from app.models.city import City

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """主页"""
    # 获取最新的6个城市
    cities = City.query.order_by(City.created_at.desc()).limit(6).all()
    return render_template('index.html', cities=cities)
