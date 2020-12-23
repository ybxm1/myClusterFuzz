# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import os, stat
import os.path
import pymysql

createjob = Blueprint('createjob', __name__)

pref_path = "/home/ybxm/myClusterFuzz/MyServer/jobprojects/"

def exec_sql(sql):
    conn = pymysql.connect(host="localhost", user="test", password="test", database="fuzz", charset="utf8")
    # 创建一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()  # it must exist, or insert and update you can't use.
    results = cursor.fetchall()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    print(results)
    return results

# Todo 将任务信息存入job中，然后将固件存入指定的目录下
@createjob.route('/', methods=["POST"])
def create_job():
    file = request.files.get('file')
    # file.read()
    job_info = request.form.to_dict()
    jobname = job_info.get("jobname")
    fuzz = job_info.get("fuzz")
    botnum = job_info.get("botnum")
    runtime = job_info.get("runtime")
    execname = job_info.get("exec")
    print(job_info)

    jobpath = pref_path + jobname
    file_save_path = jobpath + "/" + jobname + ".zip"
    if os.path.isdir(jobpath):
        print("任务已存在！")
        return jsonify({
            'msg': '任务已存在！'
        }), 403

    # create three catalog
    try:
        crash_path = jobpath + "/crashs/"
        info_path = jobpath + "/info/"
        seeds_path = jobpath + "/seeds/"
        os.makedirs(jobpath)
        os.makedirs(crash_path)
        os.makedirs(info_path)
        os.makedirs(seeds_path)
    except Exception as e:
        print("create_job()目录创建失败!")
        print(e)
        return jsonify({
            'msg': '任务目录创建失败'
        }), 500

    insert_job_sql = "insert into jobs values(default, '" + jobname + "', '" + fuzz + "'," + botnum + "," + \
                     botnum + ", 0," + runtime + ", '" + execname + "', '" + jobpath + "', 0, default)"
    print(insert_job_sql)
    # insert into jobs() values( default, "test1", "libfuzzer", 1, 0, 1, 60, "handshake-fuzzer",
    # "/home/ybxm/myClusterFuzz/MyServer/jobprojects/test", 1, default);
    try:
        file.save(file_save_path)
        exec_sql(insert_job_sql)
    except Exception as e:
        print("create_job() 创建任务失败！")
        print(e)
        return jsonify({
            'msg': '任务创建失败'
        }), 500

    return jsonify({
        'msg': '任务创建成功'
    }), 200



# https://www.cnblogs.com/yanshanketang/p/10746697.html  // get file and formdata together



