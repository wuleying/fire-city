"""
认证路由
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册路由"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # 表单验证
        if not all([username, email, password, password_confirm]):
            flash('请填写所有必填字段')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('两次输入的密码不一致')
            return redirect(url_for('auth.register'))
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已注册')
            return redirect(url_for('auth.register'))
        
        # 创建新用户
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录路由"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not all([username, password]):
            flash('请填写所有必填字段')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """退出登录路由"""
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码路由"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        new_password_confirm = request.form.get('new_password_confirm')
        
        if not all([old_password, new_password, new_password_confirm]):
            flash('请填写所有必填字段')
            return redirect(url_for('auth.change_password'))
        
        if not current_user.verify_password(old_password):
            flash('原密码错误')
            return redirect(url_for('auth.change_password'))
        
        if new_password != new_password_confirm:
            flash('两次输入的新密码不一致')
            return redirect(url_for('auth.change_password'))
        
        current_user.password = new_password
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('main.index'))
    
    return render_template('auth/change_password.html')
