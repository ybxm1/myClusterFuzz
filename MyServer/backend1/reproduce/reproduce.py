# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import os, stat
import os.path
import pymysql

reproduce = Blueprint('reproduce', __name__)

pref_path = "/home/ybxm/myClusterFuzz/MyServer/jobprojects/"
mysql_table_head_repRuning = ["id", "name", "crashname", "createtime"]
mysql_table_head_repCompleted = ["id", "name", "crashname", "isfixed", "createtime"]

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

@reproduce.route('/', methods=['POST'])
def create_reproduce():
    file = request.files.get('file')
    # file.read()
    job_info = request.form.to_dict()
    jobname = job_info.get("jobname")
    fuzz = job_info.get("fuzz")
    crashname = job_info.get("crashname")
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
        os.makedirs(jobpath)
    except Exception as e:
        print("create_reproduce()目录创建失败!")
        print(e)
        return jsonify({
            'msg': '任务目录创建失败'
        }), 500

    insert_job_sql = "insert into reproduce values(default, '" + jobname + "', '" + fuzz + "', '"\
                     + crashname + "', '" + execname + "', '" + jobpath + "', 0, 0, 0, default)"
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
        'msg': (jobname + '任务创建成功')
    }), 200


@reproduce.route('/runing/<page>', methods=['GET'])
def get_rep_running(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_rep_runing_sql = "select id, name, crashname, createtime from reproduce where completed = 0"
    get_rep_runing_total = "select count(*) from reproduce where completed = 0"
    try:
        res = exec_sql(get_rep_runing_sql)
        count = exec_sql(get_rep_runing_total)[0][0]
    except Exception as e:
        print("get_rep_runing fail!")
        print(e)
        return jsonify({
            'msg': '任务查询失败！'
        }), 500
    # data = ({"id":2, "name":'test2', "fuzzer":'libfuzzer'},)
    page_start = (p-1) * 8  # 一页显示８条记录
    page_end = p * 8 - 1
    if page_end > count - 1:  # 比较数组中的下标序列
        page_end = count - 1
    if page_start >= count:
        return jsonify({'msg': '请求任务不存在！'}), 403
    data = list()
    for i in range(page_start, page_end + 1):
        dict = {}
        num = 0
        for j in res[i]:
            dict[mysql_table_head_repRuning[num]] = j
            num = num + 1
        data.append(dict)
    # print(data)
    return jsonify({"data": list(data), "count": count}), 200


@reproduce.route('/complete/<page>', methods=['GET'])
def get_rep_complete(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_rep_complete_sql = "select id, name, crashname, isfixed, createtime from reproduce where completed = 1"
    get_rep_complete_total = "select count(*) from reproduce where completed = 1"
    try:
        res = exec_sql(get_rep_complete_sql)
        count = exec_sql(get_rep_complete_total)[0][0]
    except Exception as e:
        print("get_rep_complete fail!")
        print(e)
        return jsonify({
            'msg': '任务查询失败！'
        }), 500
    page_start = (p-1) * 8  # 一页显示８条记录
    page_end = p * 8 - 1
    if page_end > count - 1:  # 比较数组中的下标序列
        page_end = count - 1
    if page_start >= count:
        return jsonify({'msg': '请求任务不存在！'}), 403
    data = list()
    for i in range(page_start, page_end + 1):
        dict = {}
        num = 0
        for j in res[i]:
            dict[mysql_table_head_repCompleted[num]] = j
            num = num + 1
        if dict["isfixed"] == 0:
            dict["isfixed"] = "漏洞未修复"
        elif dict["isfixed"] == 1:
            dict["isfixed"] = "漏洞已修复"
        data.append(dict)
    print(res)
    print(count)
    print(data)
    return jsonify({"data": list(data), "count": count}), 200

