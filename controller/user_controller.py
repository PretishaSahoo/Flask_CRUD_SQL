from app import app
from model import user_model
from flask import request
from flask_cors import CORS
from flask import  jsonify , send_file
from datetime import datetime

CORS(app)

@app.route("/user/getall" , methods=["GET"])
def user_getall_controller():
    obj=user_model.user_model()
    return obj.user_getall()

@app.route("/user/get" , methods=["GET"])
def user_get_controller():
    limit = request.args.get('limit')
    page = request.args.get('page')
    obj=user_model.user_model()
    return obj.user_get(limit , page)
#http://127.0.0.1:5000/user/get?page=1&limit=3


@app.route("/user/add" , methods=["POST"])
def user_add_controller():
    obj=user_model.user_model()
    return obj.user_add(request.json)

@app.route("/user/edit/<id>" , methods=["PATCH"])
def user_edit_controller(id):
    obj=user_model.user_model()
    return obj.user_edit(id ,request.json)

@app.route("/user/delete/<id>" , methods=["DELETE"])
def user_delete_controller(id):
    obj=user_model.user_model()
    return obj.user_delete(id)

@app.route("/user/<uid>/upload/avtar" , methods=['PUT'])
def user_upload(uid):
    file = request.files['avatar']
    filename, extension = file.filename.rsplit('.', 1)
    mydate = str(datetime.now().timestamp()).replace('.' , "")
    fileuniqueName = filename+mydate
    filepath = f"Uploads/{fileuniqueName}.{extension}"
    file.save(filepath)
    obj=user_model.user_model()
    return obj.file_upload( filepath , uid)

@app.route("/Uploads/<filename>" , methods=['GET'])
def user_getavatar(filename):
    return  send_file(f"Uploads/{filename}")

@app.route("/user/login" , methods = ["POST"])
def user_login():
    obj = user_model.user_model() 
    return obj.login(request.data)