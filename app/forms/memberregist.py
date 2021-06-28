from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    phone = StringField('电话', validators=[DataRequired(),Regexp(r'1[34578]\d{9}',0,'请输入正确的手机号码')])
    company = SelectField('所属单位',choices=[('技术交易所有限公司', '技术交易所有限公司'), ('上海东部科技成果转化有限公司', '上海东部科技成果转化有限公司'), ('全国高校技术市场有限公司', '全国高校技术市场有限公司')])
    # company = StringField('所属单位')
    branch = SelectField('所属支部',choices=[('技术转移党支部', '技术转移党支部')])
    submit = SubmitField('提交')