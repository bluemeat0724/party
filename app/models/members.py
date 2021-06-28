from app.models import db,Base
from sqlalchemy import String,Float,Integer,Boolean


class Member(Base):
    __tablename__='members'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(32),comment='姓名')
    phone = db.Column(String(32),comment='手机号码')
    company = db.Column(String(64),comment='单位')
    branch = db.Column(String(64),comment='党支部')
    openid = db.Column(String(255),comment='openid')
    confirmed = db.Column(Boolean,default=False)
    chargeid = db.Column(String(255))


    