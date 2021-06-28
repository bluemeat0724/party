from flask import Blueprint

api = Blueprint('api_1_0',__name__)


from app.apis import registration,member_manage,file

