"""
城市评分和评论模型
"""
from datetime import datetime
from app import db

class CityReview(db.Model):
    """城市评分和评论模型"""
    __tablename__ = 'city_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1-5分
    content = db.Column(db.Text, nullable=False)  # 评论内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    city = db.relationship('City', backref=db.backref('reviews', lazy='dynamic', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))
    
    def __init__(self, city_id, user_id, score, content):
        self.city_id = city_id
        self.user_id = user_id
        self.score = score
        self.content = content
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'city_id': self.city_id,
            'user_id': self.user_id,
            'score': self.score,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<CityReview {self.id}>'
