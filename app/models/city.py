"""
城市模型
"""
from datetime import datetime
from app import db

class City(db.Model):
    """城市模型类"""
    __tablename__ = 'cities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    weather = db.Column(db.String(64))
    livability_score = db.Column(db.Float)  # 宜居程度评分(0-10)
    suitable_crowd = db.Column(db.String(256))  # 适合人群
    
    # 生活成本
    cost_of_living = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # 每月生活成本（不含房租）
    housing_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # 每月房租或房贷
    
    # 交通设施
    has_high_speed_rail = db.Column(db.Boolean, default=False)
    has_subway = db.Column(db.Boolean, default=False)
    has_airport = db.Column(db.Boolean, default=False)
    
    # 配套设施评分(0-10)
    medical_score = db.Column(db.Float)  # 医疗配套
    education_score = db.Column(db.Float)  # 教育配套
    life_score = db.Column(db.Float)  # 生活配套
    
    # 房价信息
    avg_house_price = db.Column(db.Integer)  # 平均房价(元/平方米)
    house_types = db.Column(db.String(256))  # 房子类型，逗号分隔
    house_sizes = db.Column(db.String(256))  # 房子面积范围，逗号分隔
    house_price_range = db.Column(db.String(128))  # 房价范围
    house_description = db.Column(db.Text)  # 房子描述
    
    # 创建者信息
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('cities', lazy='dynamic'))
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, code, description=None, image_url=None, weather=None,
                 livability_score=None, suitable_crowd=None, has_high_speed_rail=False,
                 has_subway=False, has_airport=False, medical_score=None,
                 education_score=None, life_score=None, avg_house_price=None,
                 house_types=None, house_sizes=None, house_price_range=None,
                 house_description=None, creator_id=None, cost_of_living=0.00,
                 housing_cost=0.00):
        self.name = name
        self.code = code
        self.description = description
        self.image_url = image_url
        self.weather = weather
        self.livability_score = livability_score
        self.suitable_crowd = suitable_crowd
        self.has_high_speed_rail = has_high_speed_rail
        self.has_subway = has_subway
        self.has_airport = has_airport
        self.medical_score = medical_score
        self.education_score = education_score
        self.life_score = life_score
        self.avg_house_price = avg_house_price
        self.house_types = house_types
        self.house_sizes = house_sizes
        self.house_price_range = house_price_range
        self.house_description = house_description
        self.creator_id = creator_id
        self.cost_of_living = cost_of_living
        self.housing_cost = housing_cost
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'image_url': self.image_url,
            'weather': self.weather,
            'livability_score': self.livability_score,
            'suitable_crowd': self.suitable_crowd,
            'has_high_speed_rail': self.has_high_speed_rail,
            'has_subway': self.has_subway,
            'has_airport': self.has_airport,
            'medical_score': self.medical_score,
            'education_score': self.education_score,
            'life_score': self.life_score,
            'avg_house_price': self.avg_house_price,
            'house_types': self.house_types,
            'house_sizes': self.house_sizes,
            'house_price_range': self.house_price_range,
            'house_description': self.house_description,
            'creator_id': self.creator_id,
            'cost_of_living': float(self.cost_of_living) if self.cost_of_living else 0.00,
            'housing_cost': float(self.housing_cost) if self.housing_cost else 0.00,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<City {self.name}>'
