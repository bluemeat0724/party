from . import api
from flask import jsonify,render_template,request,redirect,current_app,url_for
import requests
from app.secure import APPID,APPSECRET
from app.utils.wechat import *
import json
from app.forms.memberregist import RegistrationForm
from app.models.members import Member
from app.models.users import Userinfo
from app import db
from app.utils.wechat import gettoken


REDIRECT_URI = 'http%3A//yy-test.stte.com/openid'
SCOPE='snsapi_userinfo'

@api.route('/')
def main():
    return render_template('index.html')

@api.route('/gettoken')
def get_token():
    return renewtoken()


@api.route('/red')
def red():
    source_url = 'https://open.weixin.qq.com/connect/oauth2/authorize' \
                 + '?appid={APPID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}' \
                 + '#wechat_redirect'
    url = source_url.format(APPID=APPID, REDIRECT_URI=REDIRECT_URI, SCOPE=SCOPE)
    print(url)
    return redirect(url)  # 重定向

    # return render_template('index.html')

@api.route('/openid')
def getopenid():
    code = request.args.get('code')
    openid, access_token = getuserid(code)
    print(openid)
    #openid获取失败仍跳转信息登记页
    if openid is None:#测试
        openid='empty'
        access_token='test'
        return redirect(url_for('api_1_0.memberreg',openid=openid,access_token=access_token))
    else:
        member = Member.query.filter_by(openid=openid).first()
        if member is not None:
            return render_template('message.html', msg='您已提交过信息，感谢您的配合。',openid=openid)
        else:
            return redirect(url_for('api_1_0.memberreg',openid=openid,access_token=access_token))


@api.route('/memberregist',methods=['GET','POST'])
def memberreg():
    openid = request.args.get('openid')
    access_token = request.args.get('access_token')
    print(request.args.to_dict())
    if openid=='exist':
        return render_template('message.html', msg='您已提交过信息，感谢您的配合。', openid=openid)
    form = RegistrationForm()
    if form.validate_on_submit():
        partymember = Member(
            name=form.name.data,
            phone=form.phone.data,
            company=form.company.data,
            branch = form.branch.data,
            openid = openid if openid is not None else 'empty'
        )
        try:
            db.session.add(partymember)
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
        userinfoparse = getuserinfo(access_token,openid)
        openid = userinfoparse.get('openid')
        nickname = userinfoparse.get('nickname')
        sex = userinfoparse.get('sex')
        sex = sex if sex is not None else 0
        headimgurl = userinfoparse.get('headimgurl')
        city = userinfoparse.get('city')
        province = userinfoparse.get('province')
        country = userinfoparse.get('country')
        unionid = userinfoparse.get('unionid')
        timeinsert = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(nickname)
        adduser_sql='''INSERT INTO userinfo (create_time, update_time, openid, sex, province, city, country, headimgurl, unionid) VALUES ('{}','{}', '{}','{}','{}','{}','{}','{}', '{}')'''.format(timeinsert,timeinsert,openid,sex,province,city,country,headimgurl,unionid)
        print(adduser_sql)
        try:
            connection = db.engine.connect()
            connection.execute(adduser_sql)
            connection.close()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()

        return render_template('message.html',msg='登记已完成，感谢您的配合。')
    # return render_template('register.html',form=form)
    return render_template('weuiregist.html',form=form)


@api.route('/getuserinfo',methods=['GET','POST'])
def getUserinfo():
    code = request.args.get('code')
    openid,access_token=getuserid(code)
    # 第三步：刷新access_token（如果需要）

    # 第四步：拉取用户信息(需scope为 snsapi_userinfo)
    source_url = 'https://api.weixin.qq.com/sns/userinfo' \
                 + '?access_token={ACCESS_TOKEN}&openid={OPENID}&lang=en_US'
    useinfo_url = source_url.format(ACCESS_TOKEN=access_token, OPENID=openid)
    resp = requests.get(useinfo_url)
    resp.encoding = 'utf-8'
    data = json.loads(resp.text)
    userinfo = {
        'nickname': data['nickname'],
        'sex': data['sex'],
        'province': data['province'],
        'city': data['city'],
        'country': data['country'],
        'headimgurl': data['headimgurl']
    }
    return jsonify(userinfo)

@api.route('/msg',methods=['GET','POST'])
def msg():
    msg='呵呵'
    return render_template('thanks.html',msg=msg)
