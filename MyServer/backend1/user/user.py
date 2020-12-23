# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
# from bson.objectid import ObjectId, InvalidId


user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def do_login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    # if user is None:
    #     return jsonify({'msg': '用户不存在'}), 403
    # if user['password'] != password:
    #     return jsonify({'msg': '密码错误'}), 403
    if username == "admin" and password == "admin":
        return jsonify({'msg': '登陆成功', 'token': username, 'info': username, 'username': username}), 200
    else:
        return jsonify({'msg': '用户名或密码错误，请重试！'}), 403



"""
@login.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    info = request_data['info']
    users.insert_one({'username': username, 'password': password, 'info': info}), 201


@login.route('/info', methods=['POST'])
def get_info():
    request_data = request.get_json()
    user_id = request_data['token']
    try:
        user = users.find_one({'_id': ObjectId(user_id)})
    except InvalidId:
        return jsonify({
            'msg': '用户ID错误'
        }), 401
    return jsonify({
        'info': user['info'],
        'username': user['username']
    }), 200


@login.route('/users', methods=['GET'])
def get_users():
    data = request.values
    page = int(data['page'])
    page -= 1
    if page <= 0:
        page = 0
    page_size = int(data['pageSize'])
    result = users.find().skip(page*page_size).limit(page_size)
    count = users.find().count()
    return jsonify({'users': list(result), 'count': count}), 200
"""
