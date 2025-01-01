"""
导入所有模型
"""
from app.models.user import User
from app.models.city import City
from app.models.review import CityReview

__all__ = ['User', 'City', 'CityReview']
