#!/usr/bin/python
from flask import Flask
from user import user
from job import job
from fuzz import fuzz
from crash import crash
from reproduce import reproduce

 
app=Flask(__name__) #创建1个Flask实例
 
@app.route('/')      #路由系统生成 视图对应url,1. decorator=app.route() 2. decorator(first_flask)
def first_flask():    #视图函数
    return 'Hello World'  #response

@app.route('/login', methods=['GET', 'POST']) 
def login():
    return "welcome"

 
if __name__ == '__main__':
    app.run(host="localhost", port="5001")              #启动socket
