import cv2
from flask import Flask , render_template, Response,session,request,redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from website import create_app
import random
from string import ascii_uppercase
from test4 import VideoCamera
import os
from werkzeug.utils import secure_filename
from website import create_app

from datetime import datetime
from demo import *

app=create_app()


socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code
@app.route('/')
def index():
    return render_template('h1.html')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home1.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home1.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home1.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("index.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("views.home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")




# #upload image to this folder :
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///img.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['UPLOAD_FOLDER'] = "C:\\Users\\kyath\\OneDrive\\Desktop\\STRATAGEM\\Start Fresh\\Start Fresh\\images"

@app.route('/index3')

def index3():
    return render_template('index3.html')

def gen3(test4):
    while True:
        frame4=test4.try4()
        yield(b'--frame\r\n'
              b'Content-Type : video/mp4\r\n\r\n'+ frame4
              + b'\r\n\r\n')
        

@app.route('/video_feed3')
def video_feed3():
     return Response(gen3(VideoCamera()),
         mimetype='multipart/x-mixed-replace; boundary=frame')
    

# @app.route('/register')
# def hello_world():
#     return render_template("register.html")


# @app.route('/upload', methods=['POST'])
# def upload():
#     if(request.method=='POST'):
#         '''Add entry to the database'''
#         name = request.form.get('name')
#         email = request.form.get('email')
#         age = request.form.get('age')
#         mobileno = request.form.get('mobileno')
#         blood = request.form.get('blood')
#         date = datetime.now()
#         pic = request.files['pic']
#         if not pic:
#             return 'No pic uploaded!', 400

#         filename = secure_filename(pic.filename)
#         mimetype = pic.mimetype
#         if not filename or not mimetype:
#             return 'Bad upload!', 400

#         img = Info(name=name, mobileno = mobileno, age=age, blood = blood ,email = email,img=pic.read(), filename=filename, mimetype=mimetype, date = date)
#         db.session.add(img)
#         db.session.commit()
#         readBlobData(filename)
    


#     return 'Img Uploaded!', 200

# # @app.route('/temp', methods=['GET', 'POST'])
# # def temp():
# #     name1 = 'aryan.png'
# #     return render_template("temp.html", name1 = name1)

# @app.route('/<string:filename>')
# def get_img(filename):
#     img = Info.query.filter_by(filename=filename).first()
#     if not img:
#         return 'Img Not Found!', 404

#     return Response(img.img, mimetype=img.mimetype)


if __name__ == '__main__' :
    # app.run(host='0.0.0.0',port='5000',debug=True)
    socketio.run(app, debug=True)
