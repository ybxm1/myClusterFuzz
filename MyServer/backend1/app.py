# coding:utf-8
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from user import user # import的是py脚本
from createjob import createjob
from nodes import nodes
from joblist import joblist
from reproduce import reproduce
from crashes import crashes
import os

# init_cases()  # 加载用例信息

app = Flask(__name__, template_folder='dist', static_folder='dist', static_url_path='')  # 可以处理前端的文件，接收来自浏览器的前端请求
CORS(app)  # Todo 开发时添加, 用于解决跨域问题
# app.json_encoder = JSONEncoder
app.config["JSON_AS_ASCII"] = False
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(createjob, url_prefix='/createjob')
app.register_blueprint(nodes, url_prefix='/nodes')
app.register_blueprint(joblist, url_prefix='/joblist')
app.register_blueprint(reproduce, url_prefix='/reproduce')
app.register_blueprint(crashes, url_prefix='/crashes')


@app.route('/')
def index():
    return "hello world!"

"""
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
"""


if __name__ == "__main__":
    app.run(host="localhost", port="5000")  
    # app.run(host="0.0.0.0", port="5000")  # 远程访问的时候用的
