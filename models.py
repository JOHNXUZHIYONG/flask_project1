from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique = True)
    # join_time = db.Column(db.Datetime, default = datetime.now)

class QuestionModel(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(UserModel,backref='questions')

class PriceList(db.Model):
    __tablename__='price_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    item = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable=False)


class Order(db.Model):
    __tablename__='order'
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    item1 = db.Column(db.String(100), nullable = False)
    status1 = db.Column(db.String(100), nullable = False)
    laser_scanner1 = db.Column(db.String(100), nullable=False)
    sentencing_time1 = db.Column(db.String(200), nullable=False)
    verify_time1 = db.Column(db.String(200))
    final_time1 = db.Column(db.String(200))

    # item2 = db.Column(db.String(100), nullable = False)
    # quantity2 = db.Column(db.Integer, nullable = False)
    # price2 = db.Column(db.Float, nullable=False)
    # item3 = db.Column(db.String(100), nullable = False)
    # quantity3 = db.Column(db.Integer, nullable = False)
    # price3 = db.Column(db.Float, nullable=False)
    # total_price = db.Column(db.Float, nullable=False)