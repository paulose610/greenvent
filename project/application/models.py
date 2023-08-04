from application.database import db
from main import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    uname=db.Column(db.String(length=30),nullable=False,unique=True)
    pswdhash=db.Column(db.String(length=60),nullable=False)
    role=db.Column(db.String(length=10),nullable=False,default='User')
    cart = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, *args, **kwargs):
        super(user, self).__init__(*args, **kwargs)
        if self.role == "User" and not self.cart:
            cart = Cart()
            db.session.add(cart)
            self.cart = cart
            db.session.commit()


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.pswdhash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.pswdhash, attempted_password)

class cat(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    cname=db.Column(db.String(length=30),nullable=False,unique=True)
    products = db.relationship('prod', backref='cat', lazy=True)

class prod(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    catid = db.Column(db.Integer(), db.ForeignKey('cat.id',name='fkpc'), nullable=False)
    pname=db.Column(db.String(length=30),nullable=False,unique=True)    
    price = db.Column(db.Float, nullable=False)
    unit=db.Column(db.String(length=15),nullable=False)
    qty=db.Column(db.Integer(),nullable=False,default=0)
    stock=db.Column(db.Integer(),nullable=False,default=20)
    sold=db.Column(db.Integer(),nullable=False)



class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pname = db.Column(db.String(length=15), nullable=False)
    Pid = db.Column(db.Integer, db.ForeignKey('prod.id', name='fkpid'))
    qty = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(length=15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', name='fkuid'), nullable=False)
    no=db.Column(db.Integer(),nullable=False)