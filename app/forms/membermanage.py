from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class MemberfiltForm(FlaskForm):
    text = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    company = SelectField('所属单位',choices=[('stex', '技术交易所有限公司'), ('easttech', '上海东部科技成果转化有限公司'), ('gaoxiao', '全国高校技术市场有限公司')])
    branch = SelectField('所属支部',choices=[('jszy', '技术转移党支部')])
    submit = SubmitField('搜索')