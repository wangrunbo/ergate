from flask import Blueprint, make_response
from app.model import *
from app import db

data = Blueprint('data', __name__, url_prefix='/api/data')


@data.route('/create_db', methods=['GET', 'POST'])
def create_db():
    """
    モデルからDBの生成
    :return:
    """
    db.create_all()

    db.session.add(Sex('未设定'))
    db.session.add(Sex('男性'))
    db.session.add(Sex('女性'))

    db.session.add(UserStatus('未激活'))
    db.session.add(UserStatus('一般会员'))
    db.session.add(UserStatus('锁定'))
    db.session.add(UserStatus('删除'))

    db.session.add(CorporationStatus('未激活'))
    db.session.add(CorporationStatus('一般法人'))
    db.session.add(CorporationStatus('锁定'))
    db.session.add(CorporationStatus('删除'))

    db.session.add(ValueType('数字'))
    db.session.add(ValueType('文字'))
    db.session.add(ValueType('フラグ'))
    db.session.add(ValueType('時間'))
    db.session.add(ValueType('配列'))
    db.session.add(ValueType('辞書'))

    db.session.add(Setting('SITE_NAME', 'サイト名'))

    db.session.commit()

    return 'db_created'


@data.route('/test', methods=['GET', 'POST'])
def test():
    user = User.query.first()

    user.reset_secret_key()

    return 'reset complete'
