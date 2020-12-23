# coding:utf-8
# from pymongo import MongoClient
from flask import Blueprint, jsonify, request
import datetime
import pymysql
import os

nodes = Blueprint('nodes', __name__)
mysql_table_head = ["id", "name", "ip", "men", "corenum", "isfree", "surplustime"]

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

# Todo 删除死亡节点
@nodes.route('/<page>', methods=['GET'])
def get_nodelist(page):
    # page = ObjectId(page)
    p = int(page)
    print(p)
    get_node_list_sql = "select * from nodes"
    get_node_total = "select count(*) from nodes"
    try:  # Todo 当数据库中没有一条数据的时候，就会报错
        res = exec_sql(get_node_list_sql)
        count = exec_sql(get_node_total)[0][0]
    except Exception as e:
        print("get_nodelist() fail!")
        print(e)
        return jsonify({
            'msg': '节点列表查询失败！'
        }), 500

    page_start = (p - 1) * 8  # 一页显示８条记录
    page_end = p * 8 - 1
    if page_end > count - 1:  # 比较数组中的下标序列
        page_end = count - 1
    if page_start >= count:
        return jsonify({'msg': '请求的节点列表不存在！'}), 403
    data = list()
    # mysql_table_head = ["id", "name", "ip", "men", "corenum", "isfree", "surplustime"]
    for i in range(page_start, page_end + 1):
        dict = {}
        for j in range(0, 7):
            dict[mysql_table_head[j]] = res[i][j]
            if j == 5:
                if res[i][j] == 0:
                    dict[mysql_table_head[j]] = "空闲"
                else:
                    dict[mysql_table_head[j]] = "繁忙"
            if j == 6:
                if res[i][5] == 0:
                    dict[mysql_table_head[j]] = 0
                    continue
                if res[i][5] == -1:
                    dict[mysql_table_head[j]] = "<30s"
                    continue
                get_job_run_time = "select time from jobs where id = " + str(res[i][5])
                time = exec_sql(get_job_run_time)[0][0]
                print((datetime.datetime.now() - res[i][6]).seconds)
                print(time)
                dict[mysql_table_head[j]] = time - (datetime.datetime.now() - res[i][6]).seconds

        data.append(dict)
    # print(data)
    return jsonify({"data": list(data), "count": count}), 200
