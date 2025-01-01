"""
城市路由
"""
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
from app import db
from app.models.city import City

bp = Blueprint('city', __name__, url_prefix='/city')

def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/')
def index():
    """城市列表页面"""
    page = request.args.get('page', 1, type=int)
    pagination = City.query.order_by(City.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    cities = pagination.items
    return render_template('city/index.html', cities=cities, pagination=pagination)

@bp.route('/<int:id>')
def detail(id):
    """城市详情页面"""
    city = City.query.get_or_404(id)
    return render_template('city/detail.html', city=city)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """创建城市信息"""
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        description = request.form.get('description')
        weather = request.form.get('weather')
        livability_score = request.form.get('livability_score', type=float)
        suitable_crowd = request.form.get('suitable_crowd')
        has_high_speed_rail = bool(request.form.get('has_high_speed_rail'))
        has_subway = bool(request.form.get('has_subway'))
        has_airport = bool(request.form.get('has_airport'))
        medical_score = request.form.get('medical_score', type=float)
        education_score = request.form.get('education_score', type=float)
        life_score = request.form.get('life_score', type=float)
        avg_house_price = request.form.get('avg_house_price', type=int)
        house_types = request.form.get('house_types')
        house_sizes = request.form.get('house_sizes')
        house_price_range = request.form.get('house_price_range')
        house_description = request.form.get('house_description')
        
        # 处理图片上传
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename=f'uploads/{filename}')
        
        # 创建城市记录
        city = City(
            name=name,
            description=description,
            image_url=image_url,
            weather=weather,
            livability_score=livability_score,
            suitable_crowd=suitable_crowd,
            has_high_speed_rail=has_high_speed_rail,
            has_subway=has_subway,
            has_airport=has_airport,
            medical_score=medical_score,
            education_score=education_score,
            life_score=life_score,
            avg_house_price=avg_house_price,
            house_types=house_types,
            house_sizes=house_sizes,
            house_price_range=house_price_range,
            house_description=house_description
        )
        
        db.session.add(city)
        db.session.commit()
        
        flash('城市信息添加成功')
        return redirect(url_for('city.detail', id=city.id))
    
    return render_template('city/create.html')

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """编辑城市信息"""
    city = City.query.get_or_404(id)
    
    if request.method == 'POST':
        # 更新城市信息
        city.name = request.form.get('name')
        city.description = request.form.get('description')
        city.weather = request.form.get('weather')
        city.livability_score = request.form.get('livability_score', type=float)
        city.suitable_crowd = request.form.get('suitable_crowd')
        city.has_high_speed_rail = bool(request.form.get('has_high_speed_rail'))
        city.has_subway = bool(request.form.get('has_subway'))
        city.has_airport = bool(request.form.get('has_airport'))
        city.medical_score = request.form.get('medical_score', type=float)
        city.education_score = request.form.get('education_score', type=float)
        city.life_score = request.form.get('life_score', type=float)
        city.avg_house_price = request.form.get('avg_house_price', type=int)
        city.house_types = request.form.get('house_types')
        city.house_sizes = request.form.get('house_sizes')
        city.house_price_range = request.form.get('house_price_range')
        city.house_description = request.form.get('house_description')
        
        # 处理图片上传
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                city.image_url = url_for('static', filename=f'uploads/{filename}')
        
        db.session.commit()
        flash('城市信息更新成功')
        return redirect(url_for('city.detail', id=city.id))
    
    return render_template('city/edit.html', city=city)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """删除城市信息"""
    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    flash('城市信息已删除')
    return redirect(url_for('city.index'))

@bp.route('/search')
def search():
    """搜索城市"""
    query = request.args.get('q', '')
    if query:
        cities = City.query.filter(
            City.name.like(f'%{query}%') |
            City.description.like(f'%{query}%') |
            City.suitable_crowd.like(f'%{query}%')
        ).all()
    else:
        cities = []
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([city.to_dict() for city in cities])
    
    return render_template('city/search.html', cities=cities, query=query)
