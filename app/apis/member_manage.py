from . import api
from flask import jsonify,render_template,request,redirect,current_app,url_for,flash
from app.models.members import Member
from app import db
from sqlalchemy import or_
import time


@api.route('/memberinfo/',defaults={'page':1},methods=['GET', 'POST'])
@api.route('/memberinfo/<int:page>/',methods=['GET', 'POST'])
def membercheck(page):
    # pagination = Member.query.paginate(page, per_page=30, error_out=False)
    # members=pagination.items
    # return render_template('memberslist.html', pagination=pagination, members=members)
    pagination = Member.query.paginate(page, per_page=10)
    members = pagination.items

    if request.method == 'POST':
        if request.form.get('bash'):
            all=[m.id for m in members]
            confirmed=request.form.getlist('thecheckbox')
            for mid in all:
                Member.query.filter_by(id=mid).update({'confirmed': False})
            for cid in confirmed:
                Member.query.filter_by(id=cid).update({'confirmed':True})
            db.session.commit()
            return redirect(url_for('api_1_0.membercheck',page=page))
        elif request.form.get('submit'):
            company=request.form.get('company')
            # branch = request.form.get('branch')
            text = request.form.get('text')
            searchcom = "%{}%".format(text)
            confirmsts =  request.form.get('confirm')
            if confirmsts=='all' and company!='all':
                pagination = Member.query.filter(Member.company==company,or_(Member.name.like(searchcom),Member.branch.like(searchcom))).paginate(page, per_page=10)
                members = pagination.items
                # return render_template('memberslist.html', members=members, pagination=pagination)
            elif confirmsts!='all' and company=='all':
                pagination = Member.query.filter(Member.confirmed == confirmsts,
                                                 or_(Member.name.like(searchcom),
                                                     Member.branch.like(
                                                         searchcom))).paginate(page,
                                                                               per_page=10)
                members = pagination.items
                # return render_template('memberslist.html', members=members, pagination=pagination)
            elif confirmsts=='all' and company=='all':
                pagination = Member.query.paginate(page, per_page=10)
                members = pagination.items
            else:
                pagination = Member.query.filter(Member.company == company,Member.confirmed==confirmsts, or_(Member.name.like(searchcom),
                                                                                Member.branch.like(
                                                                                    searchcom))).paginate(page,
                                                                                                          per_page=10)
                members = pagination.items
            return render_template('memberslist.html', members=members, pagination=pagination)

        elif request.form.get('clear'):
            return redirect(url_for('api_1_0.membercheck', page=page))
    return render_template('memberslist.html', members=members,pagination=pagination)


