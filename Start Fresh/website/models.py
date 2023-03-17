from .import db
from flask_login import UserMixin 
from sqlalchemy.sql import func

class Note(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    data= db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    notes= db.relationship('Note')

class Info(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable=False)
    age = db.Column(db.Numeric, nullable=False)
    mobileno = db.Column(db.Numeric, nullable=False) 
    blood = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, unique=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(255), nullable=True)


