#!/usr/bin/python
from flask import Blueprint, request, jsonify, make_response
import pymysql
import json
import os

postinfo = Blueprint("cpost", __name__)  # url_prefix is cpost
pref_path = "/home/ybxm/myClusterFuzz/MyServer/jobprojects/"
uniqcrash = {}
# conn = pymysql.connect(host="localhost", user="test", password="test", database="fuzz", charset="utf8")
# # 创建一个可以执行SQL语句的光标对象
# cursor = conn.cursor()

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


def insert_crash(jobname):
    jobs_select_jobid_sql = "select id from jobs where name = '" + jobname + "'"
    jobid = exec_sql(jobs_select_jobid_sql)[0][0]
    print(jobid)
    for k, v in uniqcrash.items():
        crashes_insert_sql = "insert into crashes values(default, '" + v + "', " + str(jobid) + ", '" + \
                         pref_path + jobname + "/crashs', 0, default)"
        res = exec_sql(crashes_insert_sql)
        print(res)


def del_duplicate_crash_honggfuzz(jobpath, jobname):
    crashlist = os.listdir(jobpath)
    for i in crashlist:
        if "crash" in i:
            continue
        try:
            f1 = open(jobpath + "/" + i, "r")
        except Exception as e:  # 文件可能已经被删除
            print(e)
        crashinfo = f1.read()
        infolines = crashinfo.split("\n")
        f1.close()
        flag = 0
        crash_state = ""
        for j in infolines:
            if flag == 1 and "=======" not in j:
                res = j.split(" ")
                crash_state += res[1]
            if "STACK:" in j:
                flag = 1
            if flag == 1 and "=======" in j:
                break

        if crash_state in uniqcrash:
            os.remove(jobpath + "/" + i)  # 删除重复漏洞信息文件
            crashfile = i.replace("info", "crash")
            for j in crashlist:
                if j == crashfile:
                    os.remove(jobpath + "/" + j)  # 删除重复漏洞用例
                    break
        else:
            print(crash_state)
            uniqcrash[crash_state] = i  # 发生错误的具体位置：漏洞文件名

    insert_crash(jobname)



def del_duplicate_crash(jobname):
    global uniqcrash
    jobs_select_crashpath_sql = "select jobpath, fuzzer from jobs where name = '" + jobname + "'"
    res = exec_sql(jobs_select_crashpath_sql)
    jobpath = res[0][0] + "/crashs"
    fuzzer = res[0][1]
    if fuzzer == "Honggfuzz":
        del_duplicate_crash_honggfuzz(jobpath, jobname)
        return
    crashlist = os.listdir(jobpath)
    for i in crashlist:
        if "crash" in i:
            continue
        try:
            f1 = open(jobpath + "/" + i, "r")
        except Exception as e:  # 文件可能已经被删除
            print(e)
        crashinfo = f1.read()
        infolines = crashinfo.split("\n")
        f1.close()
        crashtype = 0
        del_crash = 0
        lineslen = len(infolines)
        for j in range(0, lineslen):
            if "LeakSanitizer" in infolines[j]:
                crashtype = 1
            if "AddressSanitizer" in infolines[j]:
                crashtype = 2
            if crashtype == 0:
                continue

            if "SUMMARY:" in infolines[j] and crashtype == 2:
                key = infolines[j].split("/")[-1]
                if key in uniqcrash:
                    del_crash = 1  # 该漏洞已经存在，所需要删除
                    break
                else:
                    print(key)
                    uniqcrash[key] = i  # 发生错误的具体位置：漏洞文件名
                    break

            if crashtype == 1 and "#0" in infolines[j]:  # 错误栈的前三条信息
                res1 = infolines[j].split(" ")
                leakstate = res1[5]
                res2 = infolines[j+1].split(" ")
                leakstate += res2[5]
                res3 = infolines[j+2].split(" ")
                leakstate += res3[5]
                if leakstate in uniqcrash:
                    del_crash = 1  # 该漏洞已经存在，所需要删除
                    break
                else:
                    uniqcrash[leakstate] = i  # 发生错误的具体位置：漏洞文件名
                    break

        if del_crash == 1:
            os.remove(jobpath + "/" + i)  # 删除重复漏洞信息文件
            crashfile = i.replace("info", "crash")
            for j in crashlist:
                if j == crashfile:
                    os.remove(jobpath + "/" + j)  # 删除重复漏洞用例
                    break

    insert_crash(jobname)


# you can find it with "localhost:5001/cpost/postcrash"
@postinfo.route("/postcrash", methods=["POST"])
def post_crash():
    file = request.files.get('file')
    jobname = request.form["jobname"]
    crashnum = request.form["crashnum"]  # 漏洞编号
    # print(jobname + " " + version)
    if file is None:
        # 表示没有发送文件
        return "上传漏洞用例失败！"
    # 直接使用上传的文件对象保存
    save_info_path = pref_path + jobname + "/crashs/" + crashnum  # TODO 当一个节点重复运行某个任务的时候，需要避免漏洞覆盖的情况，增加一步检测漏洞是否已经存在，已经存在就换个名字
    print(save_info_path)
    file.save(save_info_path)  # 同名文件会重写覆盖掉的

    if "info" in crashnum:
        return crashnum + "上传漏洞文件信息成功"

    # TODO 子节点上传的时候就将漏洞信息插入数据库中，其实可以等到jobs的compelted完成后再对漏洞进行去重和插入
    # jobs_select_jobid_sql = "select id from jobs where name = '" + jobname + "'"
    # jobid = exec_sql(jobs_select_jobid_sql)[0][0]
    # print(jobid)
    # crashes_insert_sql = "insert into crashes values(default, '" + crashnum + "', " + str(jobid) + ", '" + \
    #                      pref_path + jobname + "/crashs', 0, default)"
    # res = exec_sql(crashes_insert_sql)
    # print(res)
    return crashnum + "上传漏洞用例成功！"


@postinfo.route("/postinfo", methods=["POST"])
def post_info():
    file = request.files.get('file')
    node = request.form["nodename"]
    jobname = request.form["jobname"]
    surplusnum = request.form["surplusnum"]
    print(node + " " + jobname + " " + surplusnum)
    update_node_last_time(node)
    if file is None:
        # 表示没有发送文件
        return "上传日志文件失败！"
    # 直接使用上传的文件对象保存
    save_info_path = pref_path + jobname + "/info/" + node + "_" + jobname + "_" + surplusnum + ".log"
    if os.path.isfile(save_info_path):
        os.remove(save_info_path)
        print("File exist and has removed!")
    print(save_info_path)
    file.save(save_info_path)
    return "上传日志文件成功！"


@postinfo.route("/postseed", methods=["POST"])
def post_seed():
    file = request.files.get('file')
    jobname = request.form["jobname"]
    seedhnum = request.form["seedhnum"]
    if file is None:
        # 表示没有发送文件
        return "上传测试用例失败！"
    # 直接使用上传的文件对象保存
    save_info_path = pref_path + jobname + "/seeds/" + seedhnum  # TODO 当一个节点重复运行某个任务的时候，需要避免种子覆盖的情况，增加一步，将最后一部分的数字改为主节点种子池中的个数
    print(save_info_path)
    file.save(save_info_path)
    return "上传测试用例成功！"


@postinfo.route("/postjobcomplete", methods=["POST"])
def post_job_compelte():
    global uniqcrash
    jobname = request.form["jobname"]
    nodename = request.form["nodename"]

    # TODO 当任务全部完成之后，调用漏洞去重
    job_completed_num_sql = "select completenum, botnum from jobs where name = '" + jobname + "'"
    prog = exec_sql(job_completed_num_sql)
    print(prog)
    completednum = prog[0][0]
    botnum = prog[0][1]
    if completednum + 1 == botnum:  # 先完成漏洞去重，在更新状态
        uniqcrash.clear()
        print("正在漏洞去重中！")
        del_duplicate_crash(jobname)

    # 更新jobs的completenum
    jobs_update_compelted_sql = "update jobs set completenum = completenum + 1 where name = '" + jobname + "'"
    res = exec_sql(jobs_update_compelted_sql)
    print(res)

    # 更新node的jobid为0
    nodes_update_jobid_sql = "update nodes set jobid = 0 where name = '" + nodename + "'"
    res2 = exec_sql(nodes_update_jobid_sql)
    print(res2)

    jobs_select_jobid_sql = "select id from jobs where name = '" + jobname + "'"
    jobid = exec_sql(jobs_select_jobid_sql)[0][0]
    print(jobid)
    crashes_select_count_sql = "select count(*) from crashes where jobid = " + str(jobid)  # mysql中返回的是有整形和字符的区别的
    crashtotal = exec_sql(crashes_select_count_sql)[0][0]
    print(crashtotal)

    # 更新jobs的crashnum
    jobs_update_crashnum_sql = "update jobs set crashnum = " + str(crashtotal) + " where name = '" + jobname + "'"
    res5 = exec_sql(jobs_update_crashnum_sql)
    print(res5)

    print(nodename + " has complete the job: " + jobname)
    return "操作成功,任务已完成！"


@postinfo.route("/postreproducecomplete", methods=["POST"])
def post_reproduce_complete():
    jobname = request.form["jobname"]
    nodename = request.form["nodename"]
    crashname = request.form["crashname"]
    isfix = request.form["isfix"]  # python默认以str接收数据，除非是mysql中的数据,数字才会以int的形式出现
    # print(type(isfix))

    if isfix == 1:
        isfixed = '1' # 漏洞已修复
    else:
        isfixed = "0"

    # 更新reproduce中的completed和isfixed
    reproduce_update_compAndisf_sql = "update reproduce set completed = 1, isfixed = " + isfixed + " where name = '" + jobname + "'"
    print(reproduce_update_compAndisf_sql)
    res = exec_sql(reproduce_update_compAndisf_sql)
    print(res)

    # 如果漏洞已经修复，就更新crashes中的对应字段
    if isfixed == '1':
        crashes_update_isfix_sql = "update crashes set isfix = " + isfixed + " where name = '" + crashname + "'"

    # 更新node的jobid
    nodes_update_jobid_sql = "update nodes set jobid = 0 where name = '" + nodename + "'"
    res2 = exec_sql(nodes_update_jobid_sql)
    print(res2)

    print(nodename + " has complete the job: " + jobname)
    return "操作成功！"

"""
{"jobname": jobname, "nodename": nodename, "crashname": crashname, "isfix": isfix}
"""

"""
1. https://www.cnblogs.com/l-h-x/p/9026540.html  # 服务器端接收来自客户端的数据信息
"""
