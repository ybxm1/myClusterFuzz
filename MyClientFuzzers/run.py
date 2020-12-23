#!/usr/bin/python
import urllib
from urllib import request as req
import json
import os, stat
import time
import zipfile
import afl
import libfuzzer
import honggfuzz
import threading
import requests
import socket
import psutil
import logging
import multiprocessing
import shutil

hostname = socket.gethostname()
nodename = hostname + "-A1"
# crashinfo_number = 0
# crashinfo_exist = {}  # 记录已经上传的漏洞，key为漏洞名，value为crash_number
crash_number = 0
crash_exist = {}  # 记录已经上传的漏洞，key为漏洞名，value为crash_number
seed_number = 0
seed_exist = {}  # 记录已经上传的种子
time_sync = 30

pref_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/jobprojects/"
save_path = "/"  # 当前任务的path
url_get_job = "http://localhost:5001/cget/getjob?"
url_get_arch = "http://localhost:5001/cget/getarch?"
url_get_seeds = "http://localhost:5001/cget/getseeds?"
url_post_crash = "http://localhost:5001/cpost/postcrash"
url_post_info = "http://localhost:5001/cpost/postinfo"
url_post_seed = "http://localhost:5001/cpost/postseed"
url_post_jobcomplete = "http://localhost:5001/cpost/postjobcomplete"


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log/clientrun.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Start run log")


def get_job():
    ip = socket.gethostbyname(hostname)  # 直接使用会使用全局变量，在本地找不到
    cores = psutil.cpu_count()
    mem = int(psutil.virtual_memory().total/1024/1024/1024)
    data = [("nodename", nodename), ("ip", ip), ("cores", cores), ("mem", mem)]
    url = url_get_job + urllib.parse.urlencode(data)

    try:
        api_result = req.urlopen(url).read()  # api_result is bytes
    except Exception as e:
        print(e)
        return {"exist": "server_die"}
    result = json.loads(api_result)  # api_result = b'{"jobname":123}\n'  // 可以使用try块中的变量
    print("get_job()")
    print("job infromation : " + str(result))
    return result


def get_archive(type, name, fuzzername, execname):
    global save_path
    save_path = pref_path + fuzzername + "/" + name + "/"
    print(save_path)
    if os.path.exists(save_path):
        print(save_path + ": Path has existed.")  # 重复运行同一个任务，这样就可以在原来的基础上运行了。只有当资源数量不够的时候才会出现这种情况。
        return True
    else:  # 任务之前没有存在过，所以需要初始化创建多个文件，用于存放运行的数据信息
        os.makedirs(save_path)
        if type == "fuzz":
            crash_path = save_path + "crashs/"
            info_path = save_path + "info/"
            seeds_path = save_path + "seeds/"
            swap_seed = save_path + "swap_seed"
            os.makedirs(crash_path)
            os.makedirs(info_path)
            os.makedirs(seeds_path)
            os.makedirs(swap_seed)

    data = [("type", type), ("name", name)]
    url = url_get_arch + urllib.parse.urlencode(data)
    # print(url)

    f = req.urlopen(url)
    data = f.read()
    with open(save_path + name + ".zip", 'wb') as code:
        code.write(data)
    if not extract(save_path, name + ".zip", execname):
        return False
    print("固件已经下载配置完毕！")
    return True


def extract(save_path, name, execname):
    try:           # Todo 解压多种压缩包
        os.chdir(save_path)
        print(os.getcwd())
        extracting = zipfile.ZipFile(name)
        extracting.extractall()
        print(name + "解压完毕！")
        os.chmod("./" + execname, stat.S_IRWXU)  # 拥有者有全部权限(权限掩码)0o700
        return True
    except Exception as e:
        print(e)
        print("解压失败！")
        return False


def get_crash(name):  # 漏洞复现的时候使用
    pass


def fuzz(fuzzer, execname, runtime, surplusum, jobname):
    input = save_path + "seeds"
    output = save_path + "crashs"
    info = save_path + "info/"
    target = save_path + execname
    logger.info(input)
    if fuzzer == "AFL":
        # aflfuzzer = afl.AflEngine()
        # cmd = aflfuzzer.prepare(input, output, target)
        # aflfuzzer.fuzz(cmd, time)
        print("Afl run out successfully!")
    elif fuzzer == "Libfuzz":
        libfuzz = libfuzzer.LibfuzzerEngine()
        libfuzz.fuzz(input, output, info, target, runtime, surplusum, nodename, execname)  # nodename全局变量
        logger.info(jobname + " run out successfully")
        # print("Libfuzz run out successfully!")
    elif fuzzer == "Honggfuzz":
        # hongg = honggfuzz.HonggfuzzEngine()
        # cmd = hongg.prepare(input, output, target, time)
        # hongg.fuzz(cmd)
        print("Honggfuzz run out successfully!")


def reproduce():
    pass


def task_type(type, jobname, fuzzername, execname, runtime, surplusum):
    if type == "fuzz":
        # print("job: " + jobname + " is running!")
        logger.info("job: " + jobname + " is running!")
        fuzz(fuzzername, execname, runtime, surplusum, jobname)
    elif type == "reproduce":
        pass
    else:
        print("Don't know the job type.")


def submit_crashes(jobname):
    global crash_number  # 防止本地的crash命名冲突，每一轮任务完成后需要重置
    crash_path = save_path + "crashs/"
    crashlist = os.listdir(crash_path)
    # print(crashlist)
    logger.info("submit crash")
    print(crashlist)
    for i in crashlist:
        if i in crash_exist:
            continue
        if "info" in i:
            continue
        data = {"nodename": nodename, "jobname": jobname, "crashnum":\
                (jobname + "_" + nodename + "_" + "crash_" + str(crash_number))}
        res = requests.post(url_post_crash, files={"file": open(crash_path + i, 'rb')}, data=data)
        print("crash")
        print(res.text)
        # print(i)
        # print(crash_number)

        for j in crashlist:  # 发送漏洞对应的漏洞信息文件
            if ("info" + i) == j:
                datainfo = {"nodename": nodename, "jobname": jobname, "crashnum": \
                            (jobname + "_" + nodename + "_" + "info_" + str(crash_number))}
                res1 = requests.post(url_post_crash, files={"file": open(crash_path + j, 'rb')}, data=datainfo)
                print("info")
                print(res1.text)
                break

        crash_exist[i] = crash_number
        crash_number = crash_number + 1


# """
# dict.has_key(key)
# 如果键在字典dict里返回true，否则返回false
# """


def submit_info(jobname, surplusnum):
    info_path = save_path + "info/"
    data = {"nodename": nodename, "jobname": jobname, "surplusnum": surplusnum}
    infolist = os.listdir(info_path)  # filename
    print("submit bot info")
    for i in infolist:  # Todo 当一个节点重复运行某个任务的时候，需要做的是只将最新的上传。
        res = requests.post(url_post_info, files={"file": open(info_path + i, 'rb')}, data=data)
        # print(res.text)
        logger.info("上传运行日志")
        logger.info(res.text)
        print(res.text)


def submit_seeds(jobname):
    # seed_file_path = save_path + "/" + "seeds"
    global seed_number
    seed_path = save_path + "seeds/"
    seedlist = os.listdir(seed_path)
    print("submit seeds")
    for i in seedlist:
        if i in seed_exist:
            continue
        try:
            data = {"nodename": nodename, "jobname": jobname, "seedhnum": (nodename + "_" + str(seed_number))}
            res = requests.post(url_post_seed, files={"file": open(seed_path + i, 'rb')}, data=data)
            print(res.text)
            seed_exist[i] = seed_number
            seed_number = seed_number + 1
            # print(i)
            # print(seed_number)
        except Exception as e:
            print("submit_seeds() error: " + e)


def get_seeds(jobname):  # 第二步。种子同步阶段分两步走，先提交种子，在下载种子
    print("get_seeds")
    global seed_number

    # 从主节点获取种子压缩包
    data = [("jobname", jobname), ("nodename", nodename)]
    url = url_get_seeds + urllib.parse.urlencode(data)
    print(url)
    f = req.urlopen(url)
    data = f.read()
    swap_seed = save_path + "swap_seed"
    with open(swap_seed + "/seeds.zip", 'wb') as code:
        code.write(data)

    # 将种子压缩包解压
    os.chdir(swap_seed)  # 重定向目录
    print(os.getcwd())
    extracting = zipfile.ZipFile("seeds.zip")
    extracting.extractall()
    os.remove(swap_seed + "/seeds.zip")

    # 将新的种子添加到本地种子池中
    seedlist = os.listdir(save_path + "seeds")
    swap_seed_list = os.listdir(swap_seed)
    if len(swap_seed_list) == 0:
        print("no seed get")
        return
    for i in swap_seed_list:
        flag = 1
        for j in seedlist:  # 原来本地种子池中有的
            if i == j:
                flag -= 1
                break
        if flag == 1:
            shutil.move("./" + i, save_path + "seeds")
            seed_exist[i] = seed_number
            seed_number = seed_number + 1
        else:
            os.remove("./" + i)  # 目录重定向过了，定向到swap_seed中去了


def job_complete(jobname):
    data = {"jobname": jobname, "nodename": nodename}
    res = requests.post(url_post_jobcomplete, data=data)
    print(res.text)

if __name__ == '__main__':
    # 同步函数测试
    # save_path = "/home/ybxm/MyClientFuzzers/jobprojects/libfuzzer/test/1/"
    # submit_info("test", 1)
    # submit_crashes("test", 1)
    # submit_seeds("test", 1)

    while(True):   # 子节点的管理脚本将一直运行
        # 获取任务
        job = get_job()
        if job["exist"] == "no":
            print("No job to run, sleep 10s!")
            time.sleep(10)
            continue
        elif job["exist"] == "server_die":
            print("Can't connect server, please check.")
            time.sleep(60)
            continue
        else:
            print("Get job " + job["name"] + ", type = " + job["type"])

        # 下载固件
        if job["type"] == "reproduce":
            res1 = get_archive("reproduce", job["name"], job["fuzzer"], job["exec"])
            res2 = get_crash(job["name"])  # 未实现
        elif job["type"] == "fuzz":
            res1 = get_archive("fuzz", job["name"], job["fuzzer"], job["exec"])

        # 开始fuzz
        runtime = 1
        surplusum = 1
        if job["type"] == "fuzz":
            runtime = job["time"]  # if中的变量可以在if外使用
            surplusum = job["surplusnum"]

        # test libfuzz directly
        # x global save_path
        # save_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/jobprojects/Libfuzz/12-21-test/"
        # task_type("fuzz", "12-21-test", 'Libfuzz', 'handshake-fuzzer', 60, 1)

        print("thread start")
        logger.info("fuzz process start!")
        p1 = multiprocessing.Process(target=task_type, args=(job["type"], job["name"], job["fuzzer"],\
                                 job["exec"], runtime, surplusum))
        p1.start()
        # time.sleep(80)

        # fuzz类型的信息同步
        if job["type"] == "fuzz":
            # if True:  # job["type"] == "fuzz"
            crash_number = 0
            crash_exist = {}
            seed_number = 0
            seed_exist = {}
            start_time = time.time()
            while time.time() - start_time < runtime + 3:
                submit_crashes(job["name"])  # job["name"]
                submit_info(job["name"], job["surplusnum"])  # job["surplusnum"]
                submit_seeds(job["name"])
                get_seeds(job["name"])
                time.sleep(time_sync)  # 每隔30秒同步一次，可以按需要设置
            job_complete(job["name"])  # 时间一到，就会发送任务完成请求
        else:  # reproduce
            pass

        print(job["name"] + " 已经完成！")





        # start_time = time.time()
        # while(True):
        #     if time.time() - start_time > float(value) + 3.0:  # 任务执行时间到了，所以需要结束，去获取新的任务
        #         break
        #     time.sleep(20)
        #     submit_crashes(job["jobname"], job["archversion"])
        #     submit_info(job["jobname"], job["archversion"])
        #     submit_seeds(job["jobname"], job["archversion"])
        #     # get_seed()

        # resp = jsonify({"exist": "yes", "type": "reproduce", "name": rep[0][1], "fuzzer": rep[0][2],\
        #                 "crashname": rep[0][3], "exec": rep[0][4]})
        # resp = jsonify({"exist": "yes", "type": "fuzz", "name": job[0][1], "fuzzer": job[0][2],\
        #                 "time": job[0][6], "exec": job[0][7]})

        # try:  # 从主节点下载固件，并将其解压以及创建相关文件目录
        #     res = get_archive(job["archid"], job["fuzzername"], job["jobname"], job["archversion"],\
        #                       job["archname"], job["execname"])
        # except Exception as e:
        #     print("任务创建失败！")
        #     print(e)
        #     break
        # arg = job["cmd"].split(",")  # Todo 如果传入多个参数该如何解决？
        # key, value = arg[0].split(":")

        # t1 = threading.Thread(target=task_type, args=(job["type"], job["name"], job["fuzzer"],\
        #                       job["exec"], runtime, surplusum))
        # t.start() 　# 使用进程或者线程均可

        # break




# result = api_result.decode().split("'") # transform bytes to str then split
# res = result[0].split(",")
#
#
# # 得到job的参数信息
# jobname = (res[0].split("="))[1]
# fuzzername = (res[1].split("="))[1]
# cmd = (res[2].split("="))[1]
# archversion = (res[3].split("="))[1]
# print(jobname + " " + fuzzername + " " + cmd + " " + archversion)

# data = {
#     "version": archversion,
#     "archname": "openssl-fuzzer-build.zip"
# }
# datajson = json.dumps(data).encode()
# filename = save_path + data["archname"]
# urllib.request.urlretrieve(url, filename=None, reporthook=None, data=None)
# req.urlretrieve(url2, filename=filename, data=datajson)

"""
if __name__ == '__main__':
    print("downloading with urllib")
    # url = 'http://www.wzsky.net/img2013/uploadimg/20130906/1216294.jpg'
    url = 'http://music.163.com/song/media/outer/url?id=436514312.mp3'
    f = urllib.request.urlopen(url)
    data = f.read()
    # 存储位置可自定义
    with open("C:/Users/asus/Desktop/tes.mp3", 'wb') as code:
        code.write(data)
"""
"""
线程是可以创建进程的，但是线程和他创建的进程之间没有继承关系，线程的资源是共享其所依附的进程的资源，
（线程只独立拥有很少一些自己运行所需要的资源），所以线程所创建的进程的父进程是线程所依附的进程，也可
将线程理解为他所依附的进程的一段代码。
"""
"""
https://www.cnblogs.com/qq991025/p/11783588.html 文件目录操作
https://blog.csdn.net/sinat_36188088/article/details/106410754 use request.post()
"""
