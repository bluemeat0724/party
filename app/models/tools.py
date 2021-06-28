from app.models import db,Base
from sqlalchemy import String,Float,Integer,Boolean

class Token(Base):
    __tablename__='token'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    token = db.Column(String(32))