"""
应用入口文件
"""
import os
from app import create_app, db

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25000)
