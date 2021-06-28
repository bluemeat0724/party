from app.models import db,Base
from sqlalchemy import String,Float,Integer,Boolean


class Userinfo(Base):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    openid = db.Column(String(255),comment='openid')
    nickname = db.Column(String(255), comment='nickname')
    # subscribe = db.Column(Boolean,comment='订阅状态')
    sex = db.Column(Integer,comment='性别')
    province = db.Column(String(255), comment='省份')
    city = db.Column(String(255), comment='城市')
    country = db.Column(String(255), comment='国家')
    headimgurl = db.Column(String(255), comment='用户头像')
    unionid = db.Column(String(255), comment='订阅状态')
