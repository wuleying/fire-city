"""
城市评分和评论表单
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    """城市评分和评论表单"""
    score = IntegerField(
        '评分',
        validators=[
            DataRequired(message='请输入评分'),
            NumberRange(min=1, max=5, message='评分必须在1-5分之间')
        ]
    )
    content = TextAreaField(
        '评论内容',
        validators=[DataRequired(message='请输入评论内容')]
    )
