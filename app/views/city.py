"""
城市视图
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.forms.city import CityForm
from app.models.city import City
from app import db
from sqlalchemy import or_
from decimal import Decimal

# 创建蓝图
city = Blueprint('city', __name__)

@city.route('/search')
def search():
    """搜索城市"""
    query = request.args.get('q', '')
    if query:
        # 在名称和描述中搜索
        cities = City.query.filter(
            or_(
                City.name.ilike(f'%{query}%'),
                City.description.ilike(f'%{query}%')
            )
        ).all()
    else:
        cities = []
    
    return render_template('city/index.html', cities=cities, search_query=query)

@city.route('/')
def index():
    """城市列表"""
    cities = City.query.order_by(City.created_at.desc()).all()
    return render_template('city/index.html', cities=cities)

@city.route('/<int:id>')
def detail(id):
    """城市详情"""
    city = City.query.get_or_404(id)
    return render_template('city/detail.html', city=city)

@city.route('/create', methods=['GET', 'POST'])
def create():
    """创建城市"""
    form = CityForm()
    
    if form.validate_on_submit():
        city = City(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data,
            creator_id=current_user.id,
            cost_of_living=Decimal(str(form.cost_of_living.data or 0)),
            housing_cost=Decimal(str(form.housing_cost.data or 0))
        )
        
        try:
            db.session.add(city)
            db.session.commit()
            flash('城市创建成功！', 'success')
            return redirect(url_for('city.index'))
        except Exception as e:
            db.session.rollback()
            flash('城市创建失败：' + str(e), 'danger')
    
    # GET 请求或表单验证失败时显示表单
    return render_template('city/create.html', form=form)

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
        city.name = form.name.data
        city.description = form.description.data
        city.cost_of_living = Decimal(str(form.cost_of_living.data or 0))
        city.housing_cost = Decimal(str(form.housing_cost.data or 0))
        try:
            db.session.commit()
            flash('城市更新成功！', 'success')
            return redirect(url_for('.detail', id=id))
        except Exception as e:
            db.session.rollback()
            flash('城市更新失败：' + str(e), 'danger')
    
    return render_template('city/edit.html', form=form, city=city)
