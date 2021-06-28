from app.secure import APPID,APPSECRET
import requests,json
from app.secure import APPID,APPSECRET
from app.models.tools import Token
from app import db
from datetime import datetime
from flask import current_app

# def token(requset):
#     url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APPID,APPSECRET)
#     token_requests = requests.get(url)
#
#     access_token = json.loads(token_requests.text)['access_token']
#
#     return access_token

def getuserid(code):
    source_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                 + 'appid={APPID}&secret={APPSECRET}&code={CODE}&grant_type=authorization_code'
    access_token_url = source_url.format(APPID=APPID, APPSECRET=APPSECRET, CODE=code)
    resp = requests.get(access_token_url)
    data = eval(resp.text)
    print(data)
    access_token = data.get('access_token')
    openid = data.get('openid')
    return openid,access_token

def getuserinfo(access_token,openid):
    try:
        source_url = 'https://api.weixin.qq.com/sns/userinfo' \
                     + '?access_token={ACCESS_TOKEN}&openid={OPENID}&lang=en_US'
        useinfo_url = source_url.format(ACCESS_TOKEN=access_token, OPENID=openid)
        resp = requests.get(useinfo_url)
        resp.encoding = 'utf-8'
        data = json.loads(resp.text)
    except Exception as e:
        current_app.logger.debug(e)
        data={'openid':'empty'}
    return data

def gettoken():
    token_requests = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(APPID,APPSECRET))
    data = json.loads(token_requests.text)
    token = data.get('access_token')
    return token

def renewtoken():
    tokenquery=Token.query.order_by(
            db.desc('create_time')).first()
    if tokenquery is None:
        token=gettoken()
        newtoken=Token(token=token)
        try:
            db.session.add(newtoken)
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
        return token
    else:
        last=datetime.now()-tokenquery.create_time
        print(last.total_seconds())
        if last.total_seconds()>7000:
            token=gettoken()
            if token is None:
                token='test'
            newtoken = Token(token=token)
            try:
                db.session.add(newtoken)
                db.session.commit()
            except Exception as e:
                current_app.logger.debug(e)
                db.session.rollback()
            return token
        else:
            print(tokenquery.id)
            return tokenquery.token

