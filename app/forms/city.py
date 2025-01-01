"""
城市表单
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CityForm(FlaskForm):
    """城市表单"""
    name = StringField('城市名称', validators=[
        DataRequired(message='请输入城市名称'),
        Length(min=2, max=50, message='城市名称长度必须在2-50个字符之间')
    ])
    code = StringField('城市代码', validators=[
        DataRequired(message='请输入城市代码'),
        Length(min=2, max=10, message='城市代码长度必须在2-10个字符之间')
    ])
    description = TextAreaField('城市描述', validators=[
        DataRequired(message='请输入城市描述'),
        Length(min=10, max=500, message='城市描述长度必须在10-500个字符之间')
    ])
    image = FileField('城市图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片文件!')
    ])
    cost_of_living = DecimalField('生活成本', validators=[
        DataRequired(message='请输入生活成本'),
        NumberRange(min=0, max=100000, message='生活成本必须在0-100000之间')
    ])
    housing_cost = DecimalField('房屋成本', validators=[
        DataRequired(message='请输入房屋成本'),
        NumberRange(min=0, max=100000, message='房屋成本必须在0-100000之间')
    ])
    submit = SubmitField('保存')
