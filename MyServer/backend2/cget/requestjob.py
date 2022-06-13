#!/usr/bin/python
from flask import Blueprint, request, send_from_directory, jsonify, make_response
import pymysql
import datetime
import json
import os
import zipfile

requestjob = Blueprint("cget", __name__)  # 在前面的页面中已经通过register_blueprint()注册好了的

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

def update_node_last_time(name):
    update_node_info = "update nodes set last_modify_time = default where name = '" + name + "'"
    res = exec_sql(update_node_info)
    print(res)
    print("update " + name + " last modified time.")


def add_node(name, ipaddr, men, corenum):
    node_isexist_sql = "select count(*) from nodes where name = '" + name + "'"
    node_isexist = exec_sql(node_isexist_sql)[0][0]
    if node_isexist == 0:
        add_node_sql = "insert into nodes values(default, '" + name + "', '" + ipaddr + "', " + men + ", " + corenum +\
                       ", 0, default, default, default)"
        res = exec_sql(add_node_sql)
        print(res)
        print("add " + name + " to node list.")
    else:
        update_node_last_time(name)


# you can find it with "localhost:5001/cget/getjob"
@requestjob.route("/getjob", methods=["GET"])   # get是客户端向服务器请求资源，post是客户端向服务器提交数据
def get_job():
    name = request.args.get("nodename")
    ipaddr = request.args.get("ip")
    men = request.args.get("mem")
    corenum = request.args.get("cores")
    add_node(name, ipaddr, men, corenum)
    print(name + " request a job to run!")
    # update_node_last_time(name)

    # 先获取漏洞修复验证任务
    get_rep_sql = "select * from reproduce where isfetch = 0 limit 1"  # 从满足条件的结果中挑选一条记录
    rep = exec_sql(get_rep_sql)
    if len(rep) > 0:
        print(rep[0])
        resp = jsonify({"exist": "yes", "type": "reproduce", "name": rep[0][1], "fuzzer": rep[0][2],\
                        "crashname": rep[0][3], "exec": rep[0][4]})
        rep_update_isfetch_sql = "update reproduce set isfetch = 1 where id = " + str(rep[0][0])  # 数据库搜出来的int就是int
        res = exec_sql(rep_update_isfetch_sql)
        print(res)

        nodes_update_jobid_sql = "update nodes set jobid = -1 where name = '" + name + "'"
        res2 = exec_sql(nodes_update_jobid_sql)
        print(res2)
        return resp

    # 再获取模糊测试任务
    get_job_sql = "select * from jobs where surplusnum > 0 limit 1"
    job = exec_sql(get_job_sql)
    if len(job) > 0:
        print(job[0])
        fuzzer = ""
        if job[0][3] == "AFLFAST+QSYM":
            if job[0][5] == job[0][6]:
                fuzzer = fuzzer + "QSYM"
            else:
                fuzzer = fuzzer + "AFLFAST"
        elif job[0][3] == "AFL+AFLFAST+Libfuzz+Radamsa":
            if job[0][5] == 4:
                fuzzer = fuzzer + "AFL"
            elif job[0][5] == 3:
                fuzzer = fuzzer + "AFLFAST"
            elif job[0][5] == 2:
                fuzzer = fuzzer + "Libfuzz"
            else:
                fuzzer = fuzzer + "Radamsa"
        else:  # 普通模糊测试、目标点模糊测试
            fuzzer = fuzzer + job[0][3]
        resp = jsonify({"exist": "yes", "type": "fuzz", "name": job[0][1], "fuzzer": fuzzer,\
                        "time": job[0][7], "exec": job[0][8],  "surplusnum": job[0][5], "fuzztype": job[0][2]})

        job_update_sql = "update jobs set surplusnum = surplusnum - 1 where id = " + str(job[0][0])
        res1 = exec_sql(job_update_sql)
        print(res1)

        nodes_update_jobid_sql = "update nodes set jobid = " + str(job[0][0]) + " where name = '" + name + "'"
        res2 = exec_sql(nodes_update_jobid_sql)
        print(res2)

        nodes_update_fetchtime = "update nodes set fetchtime = default where name = '" + name + "'"
        res = exec_sql(nodes_update_fetchtime)
        print(res)

        return resp

    return jsonify({"exist": "no"})


@requestjob.route("/getarch", methods=["GET", "POST"])  # must use 'GET', if you use 'POST', you will get http-405
def get_archive():
    type = request.args.get("type")
    name = request.args.get("name")
    if type == "reproduce":
        sql = "select jobpath from reproduce where name = '" + name + "'"
    else:  # fuzz
        sql = "select jobpath from jobs where name = '" + name + "'"
    results = exec_sql(sql)
    # print(results)
    path = results[0][0]
    return send_from_directory(r"" + path + "", filename=name+".zip", as_attachment=True)


@requestjob.route("/getcrash", methods=["GET", "POST"])  # must use 'GET', if you use 'POST', you will get http-405
def get_crash():
    name = request.args.get("name")  # 漏洞名
    # print(name)
    sql = "select crashpath from crashes where name = '" + name + "'"
    # print(sql)
    results = exec_sql(sql)
    path = results[0][0]
    # print(path)
    return send_from_directory(r"" + path + "", filename=name , as_attachment=True)


@requestjob.route("/getseeds", methods=["GET","POST"])
def get_seed():
    jobname = request.args.get("jobname")
    nodename = request.args.get("nodename")
    sql = "select jobpath from jobs where name = '" + jobname + "'"
    results = exec_sql(sql)
    job_path = results[0][0]

    seeds_path = job_path + "/seeds"
    seedlist = os.listdir(seeds_path)
    if os.path.isfile(seeds_path + "/seeds.zip"):
        os.remove(seeds_path + "/seeds.zip")
        # print(seeds_path + "/seeds.zip")
        print("seeds zipfile exist and has removed!")

    os.chdir(seeds_path)
    f = zipfile.ZipFile(seeds_path + "/seeds.zip", "a", zipfile.ZIP_DEFLATED)
    for i in seedlist:
        if nodename in i or "zip" in i:
            continue
        f.write(i)
    f.close()
    return send_from_directory(r"" + seeds_path + "", filename="seeds.zip", as_attachment=True)  # 若没有设置好，则会报404问题

