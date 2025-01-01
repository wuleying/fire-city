"""
城市视图
"""
import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app.models.city import City
from app.models.review import CityReview
from app.forms.city import CityForm
from app.forms.review import ReviewForm
from app import db

city = Blueprint('city', __name__)

def allowed_file(filename):
    """检查文件是否允许上传"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def save_image(file):
    """保存图片文件"""
    if file:
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        # 确保上传目录存在
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        # 保存文件
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        # 返回相对路径
        return f'/static/uploads/{unique_filename}'
    return None

@city.route('/')
def index():
    """城市列表"""
    page = request.args.get('page', 1, type=int)
    pagination = City.query.order_by(City.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    cities = pagination.items
    return render_template('city/index.html', cities=cities, pagination=pagination)

@city.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建城市"""
    form = CityForm()
    if form.validate_on_submit():
        # 处理图片上传
        image_url = None
        if form.image.data:
            image_url = save_image(form.image.data)
            
        city = City(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data,
            image_url=image_url,
            cost_of_living=form.cost_of_living.data,
            housing_cost=form.housing_cost.data,
            creator_id=current_user.id
        )
        db.session.add(city)
        db.session.commit()
        flash('城市创建成功！')
        return redirect(url_for('city.index'))
    return render_template('city/create.html', form=form)

@city.route('/<int:id>')
def detail(id):
    """城市详情"""
    city = City.query.get_or_404(id)
    
    # 计算平均评分
    avg_score = db.session.query(func.avg(CityReview.score)).filter_by(city_id=id).scalar() or 0
    
    # 获取用户评论
    user_review = None
    if current_user.is_authenticated:
        user_review = CityReview.query.filter_by(
            city_id=id, user_id=current_user.id).first()
    
    # 获取所有评论
    reviews = CityReview.query.filter_by(city_id=id).order_by(
        CityReview.created_at.desc()).all()
    
    # 评论表单
    form = ReviewForm()
    
    return render_template('city/detail.html', 
                         city=city, 
                         avg_score=avg_score,
                         user_review=user_review,
                         reviews=reviews,
                         form=form)

@city.route('/<int:id>/review', methods=['POST'])
@login_required
def review(id):
    """添加评论"""
    city = City.query.get_or_404(id)
    form = ReviewForm()
    if form.validate_on_submit():
        # 检查用户是否已经评论过
        existing_review = CityReview.query.filter_by(
            city_id=id, user_id=current_user.id).first()
        if existing_review:
            flash('您已经评论过这个城市了！')
            return redirect(url_for('city.detail', id=id))
            
        review = CityReview(
            city_id=id,
            user_id=current_user.id,
            score=form.score.data,
            content=form.content.data
        )
        db.session.add(review)
        db.session.commit()
        flash('评论提交成功！')
    return redirect(url_for('city.detail', id=id))

@city.route('/search')
def search():
    """搜索城市"""
    query = request.args.get('q', '')
    if query:
        cities = City.query.filter(
            (City.name.like(f'%{query}%')) |
            (City.description.like(f'%{query}%'))
        ).all()
    else:
        cities = []
    return render_template('city/search.html', cities=cities, query=query)

@city.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """编辑城市"""
    city = City.query.get_or_404(id)
    if city.creator_id != current_user.id:
        flash('您没有权限编辑这个城市', 'warning')
        return redirect(url_for('.detail', id=id))
    
    form = CityForm(obj=city)
    if form.validate_on_submit():
        # 处理图片上传
        image_url = None
        if form.image.data:
            image_url = save_image(form.image.data)
            
        city.name = form.name.data
        city.description = form.description.data
        city.image_url = image_url
        city.cost_of_living = form.cost_of_living.data
        city.housing_cost = form.housing_cost.data
        try:
            db.session.commit()
            flash('城市更新成功！', 'success')
            return redirect(url_for('.detail', id=id))
        except Exception as e:
            db.session.rollback()
            flash('城市更新失败：' + str(e), 'danger')
    
    return render_template('city/edit.html', form=form, city=city)

@city.route('/review/<int:id>/delete', methods=['POST'])
@login_required
def delete_review(id):
    """删除评论"""
    review = CityReview.query.get_or_404(id)
    if review.user_id != current_user.id:
        flash('您没有权限删除这条评论', 'warning')
        return redirect(url_for('.detail', id=review.city_id))
    
    try:
        db.session.delete(review)
        db.session.commit()
        flash('评论删除成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash('评论删除失败：' + str(e), 'danger')
    
    return redirect(url_for('.detail', id=review.city_id))
