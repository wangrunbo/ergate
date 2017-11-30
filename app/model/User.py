import random
import string
from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt
from .UserStatus import UserStatus


class User(db.Model):
    """会員"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(12), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    target_email = db.Column(db.String(100), nullable=True)
    secret_key = db.Column(db.String(128), nullable=False, unique=True)
    tel_cert_code = db.Column(db.String(6), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    sex_id = db.Column(db.SmallInteger, db.ForeignKey('sex.id'), nullable=False, server_default='1')
    birthday = db.Column(db.DateTime, nullable=True)
    postcode = db.Column(db.String(7), nullable=True)
    prefecture_id = db.Column(db.SmallInteger, db.ForeignKey('prefectures.id'), nullable=True)
    address = db.Column(db.Text, nullable=True)
    tel = db.Column(db.String(11), nullable=True)
    user_status_id = db.Column(db.SmallInteger, db.ForeignKey('user_statuses.id'), nullable=False)
    registration_ip = db.Column(db.String(15), nullable=False)

    note = db.Column(db.Text, nullable=True, server_default=None)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP'))
    updated = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = db.Column(db.Integer, db.ForeignKey('managers.id'), nullable=True, server_default=None)

    sex = db.relationship('Sex', backref='users')
    prefecture = db.relationship('Prefecture', backref='users')
    user_status = db.relationship('UserStatus', backref='users')
    modifier = db.relationship('Manager', backref='modified_users')

    def __repr__(self):
        return f'<User {self.username}>'

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value)

    def password_identified(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True

        return False

    def is_authenticated(self):
        """一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证"""
        return True

    def is_active(self):
        """应该返回 True，除非是用户是无效的，比如因为他们的账号是被禁止"""
        return self.user_status_id == UserStatus.GENERAL

    def is_anonymous(self):
        """应该返回 True，除非是伪造的用户不允许登录系统"""
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def new_secret_key():
        secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=128))

        while User.query.filter_by(secret_key=secret_key).first():
            secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=128))

        return secret_key

    @staticmethod
    def new_uid():
        uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        while User.query.filter_by(uid=uid).first():
            uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        return uid
