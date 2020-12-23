# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import pymysql
import os


crashes = Blueprint('crashes', __name__)
mysql_table_head_crash = ["id", "name", "jobid", "crashpath", "isfix", "findtime"]


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

@crashes.route('/getcrashinfo/<jobid>', methods=['GET'])
def get_crash_info(jobid):  # 在joblist中通过jobid来获取该任务对应的所有的漏洞信息, 对漏洞信息的名称不做要求
    # print(jobid)
    get_jobpath_sql = "select jobpath from jobs where id = " + jobid
    try:
        jobpath = exec_sql(get_jobpath_sql)[0][0]  # 返回的是元组
        print(jobpath)
    except Exception as e:
        print("get_crash_info() fail!")
        print(e)
        return jsonify({
            'msg': '任务id不存在！'
        }), 500
    info_path = jobpath + "/crashs/"
    crashdata = list()
    for i in os.listdir(info_path):
        if "crash" in i:
            continue
        dict = {}
        dict["name"] = i
        crash = open(info_path + i, "r")
        dict["crash"] = crash.read()  # .replace("\n", "<br/>")
        crash.close()
        crashdata.append(dict)
    return jsonify(crashdata), 200


@crashes.route('/getsinglecrashinfo/<crashname>', methods=['GET'])
def get_single_crash_info(crashname):  # 在crash中通过crashid来获取漏洞对应的漏洞信息
    # print(crashname)
    get_crashpath_sql = "select crashpath from crashes where name = '" + crashname + "'"
    try:
        crash_path = exec_sql(get_crashpath_sql)[0][0]  # 返回的是元组
        print(crash_path)
    except Exception as e:
        print("get_single_crash_info() fail!")
        print(e)
        return jsonify({
            'msg': '漏洞id不存在！'
        }), 500
    crashdata = list()
    dict = {}
    crashinfo = crashname.replace("crash", "info")  # test2_A1_crash_1, test2_A1_info_1
    dict["name"] = crashinfo
    crash = open(crash_path + "/" + crashinfo, "r")
    dict["crash"] = crash.read()  # .replace("\n", "<br/>")
    crash.close()
    crashdata.append(dict)
    # print(list(crashdata)) 字典变数组，结果只剩下key,value被省略了
    return jsonify(crashdata), 200


@crashes.route('/fixed/<page>', methods=['GET'])
def get_crash_fixed(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_crash_fixed_sql = "select * from crashes where isfix = 1"
    get_crash_fixed_total = "select count(*) from crashes where isfix = 1"
    try:
        res = exec_sql(get_crash_fixed_sql)
        count = exec_sql(get_crash_fixed_total)[0][0]
    except Exception as e:
        print("get_crash_fixed fail!")
        print(e)
        return jsonify({
            'msg': '漏洞查询失败！'
        }), 500
    # data = ({"id":2, "name":'test2', "fuzzer":'libfuzzer'},)
    page_start = (p - 1) * 8  # 一页显示８条记录
    page_end = p * 8 - 1
    if page_end > count - 1:  # 比较数组中的下标序列
        page_end = count - 1
    if page_start >= count:
        return jsonify({'msg': '请求页面不存在！'}), 403
    data = list()
    for i in range(page_start, page_end + 1):
        dict = {}
        num = 0
        for j in res[i]:
            dict[mysql_table_head_crash[num]] = j
            num = num + 1
        data.append(dict)
    print(data)
    return jsonify({"data": list(data), "count": count}), 200


@crashes.route('/unfixed/<page>', methods=['GET'])
def get_crash_unfixed(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_crash_unfixed_sql = "select * from crashes where isfix = 0"
    get_crash_unfixed_total = "select count(*) from crashes where isfix = 0"
    try:
        res = exec_sql(get_crash_unfixed_sql)
        count = exec_sql(get_crash_unfixed_total)[0][0]
    except Exception as e:
        print("get_crash_unfixed fail!")
        print(e)
        return jsonify({
            'msg': '漏洞查询失败！'
        }), 500
    # data = ({"id":2, "name":'test2', "fuzzer":'libfuzzer'},)
    page_start = (p - 1) * 8  # 一页显示８条记录
    page_end = p * 8 - 1
    if page_end > count - 1:  # 比较数组中的下标序列
        page_end = count - 1
    if page_start >= count:
        return jsonify({'msg': '请求页面不存在！'}), 403
    data = list()
    for i in range(page_start, page_end + 1):
        dict = {}
        num = 0
        for j in res[i]:
            dict[mysql_table_head_crash[num]] = j
            num = num + 1
        data.append(dict)
    print(data)
    return jsonify({"data": list(data), "count": count}), 200



