"""
创建管理员用户
"""
from app import create_app, db
from app.models.user import User

def create_admin():
    """创建管理员用户"""
    app = create_app()
    with app.app_context():
        # 检查用户是否已存在
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin is None:
            admin = User(
                username='admin',
                email='admin@example.com',
                password='password123'
            )
            db.session.add(admin)
            db.session.commit()
            print('管理员用户创建成功！')
            print('邮箱：admin@example.com')
            print('密码：password123')
        else:
            print('管理员用户已存在')

if __name__ == '__main__':
    create_admin()
