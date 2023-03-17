from db import db


# class Img(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.Text, unique=True, nullable=False)
#     name = db.Column(db.Text, nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)

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
    date = db.Column(db.String(12), nullable=True)



