# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import pymysql
import os
# from bson.objectid import ObjectId, InvalidId


joblist = Blueprint('joblist', __name__)


mysql_table_head = ["id", "name", "fuzzer", "botnum", "surplusnum", "completenum",\
                    "time", "exec", "jobpath", "crashnum", "createtime"]

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
    # print(results)
    return results

@joblist.route('/runing/<page>', methods=['GET'])
def get_job_running(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_job_runing_sql = "select * from jobs where botnum > completenum"
    get_jobs_runing_total = "select count(*) from jobs where botnum > completenum"
    try:
        res = exec_sql(get_job_runing_sql)
        count = exec_sql(get_jobs_runing_total)[0][0]
    except Exception as e:
        print("get_job_runing fail!")
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
            dict[mysql_table_head[num]] = j
            num = num + 1
        data.append(dict)
    # print(data)
    return jsonify({"data": list(data), "count": count}), 200


@joblist.route('/complete/<page>', methods=['GET'])
def get_job_complete(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_job_complete_sql = "select * from jobs where botnum = completenum"
    get_jobs_complete_total = "select count(*) from jobs where botnum = completenum"
    try:  # Todo 当数据库中没有一条数据的时候，就会报错
        res = exec_sql(get_job_complete_sql)
        count = exec_sql(get_jobs_complete_total)[0][0]
    except Exception as e:
        print("get_job_complete fail!")
        print(e)
        return jsonify({
            'msg': '任务查询失败！'
        }), 500
    # data = ({"id":2, "name":'test2', "fuzzer":'libfuzzer'},)
    page_start = (p - 1) * 8  # 一页显示８条记录
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
            dict[mysql_table_head[num]] = j
            num = num + 1
        data.append(dict)
    # print(data)
    return jsonify({"data": list(data), "count": count}), 200


@joblist.route('/getjoblog/<jobid>', methods=['GET'])
def get_job_log(jobid):
    # print(jobid)
    get_jobpath_sql = "select jobpath from jobs where id = " + jobid
    try:
        jobpath = exec_sql(get_jobpath_sql)[0][0]  # 返回的是元组
        print(jobpath)
    except Exception as e:
        print("get_job_log() fail!")
        print(e)
        return jsonify({
            'msg': '任务id不存在！'
        }), 500
    info_path = jobpath + "/info/"
    logdata = list()
    for i in os.listdir(info_path):
        dict = {}
        dict["name"] = i
        log = open(info_path + i, "r")
        dict["log"] = log.read().replace("\n", "<br/>")
        log.close()
        logdata.append(dict)
    return jsonify(logdata), 200