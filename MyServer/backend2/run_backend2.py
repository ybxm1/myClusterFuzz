#!/usr/bin/python
from flask import Flask
from cpost import postinfo
from cget import requestjob  # from cget catalog import requestjob.py script


app = Flask(__name__)  #创建1个Flask实例
app.config["JSON_AS_ASCII"] = False
app.register_blueprint(postinfo, url_prefix="/cpost")
app.register_blueprint(requestjob, url_prefix="/cget")


# test1
@app.route('/', methods=['GET', 'POST'])      #路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
def index():    #视图函数
    return 'Hello World'  #response

# test2
@app.route('/login', methods=['GET', 'POST']) 
def login():
    return "welcome"

 
if __name__ == '__main__':
    app.run(host="localhost", port="5001")              #启动socket
