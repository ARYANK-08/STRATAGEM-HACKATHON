from flask import Blueprint, render_template, request, flash, redirect, url_for ,Response
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from demo import *
from .models import Info

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/register')
def hello_world():
    return render_template("register.html")


@auth.route('/upload', methods=['POST'])
def upload():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        mobileno = request.form.get('mobileno')
        blood = request.form.get('blood')
        date = datetime.now()
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Info(name=name, mobileno = mobileno, age=age, blood = blood ,email = email,img=pic.read(), filename=filename, mimetype=mimetype, date = date)
        db.session.add(img)
        db.session.commit()
        readBlobData(filename)
    


    return 'Img Uploaded!', 200

# @app.route('/temp', methods=['GET', 'POST'])
# def temp():
#     name1 = 'aryan.png'
#     return render_template("temp.html", name1 = name1)

@auth.route('/<string:filename>')
def get_img(filename):
    img = Info.query.filter_by(filename=filename).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
    

@auth.route("/user_profile/<string:filename>" , methods=['GET', 'POST'])
def dashboard(filename):

    post = Info.query.filter_by(filename=filename).first()
    age = math.trunc(post.age)
    mobileno = math.trunc(post.mobileno)
    date = post.date
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    date = date.strftime("%d-%b-%Y %I.%M %p")
    

    return render_template("user_profile.html", post=post, age = age, mobileno=mobileno, date=date)



@auth.route("/temp",methods=['GET', 'POST'])
def temp():
    filename = 'ash.png'
    return render_template("temp.html", filename = filename)

@auth.route('/download')
def download():
    name = 'aryan.png'
    post = Info.query.filter_by(filename=name).first()
    return send_file(BytesIO(post.img), attachment_filname=post.filename, as_attachment=True)
 
