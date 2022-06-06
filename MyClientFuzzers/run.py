#!/usr/bin/python
import urllib
from urllib import request as req
import json
import os, stat
import time
import zipfile
import afl
import aflfast
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

pref_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/jobprojects/"  # 不同的子节点需要改动的地方
afl_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/afl-2.52b/afl-fuzz"
aflfast_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/aflfast/afl-fuzz"
hogngfuzz_path = "/home/ybxm/myClusterFuzz/MyClientFuzzers/honggfuzz/honggfuzz"
save_path = "/"  # 当前任务的path
url_get_job = "http://localhost:5001/cget/getjob?"
url_get_arch = "http://localhost:5001/cget/getarch?"
url_get_seeds = "http://localhost:5001/cget/getseeds?"
url_get_rep_crash = "http://localhost:5001/cget/getcrash?"
url_post_crash = "http://localhost:5001/cpost/postcrash"
url_post_info = "http://localhost:5001/cpost/postinfo"
url_post_seed = "http://localhost:5001/cpost/postseed"
url_post_jobcomplete = "http://localhost:5001/cpost/postjobcomplete"
url_post_reproducecomplete = "http://localhost:5001/cpost/postreproducecomplete"


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log/client-" + nodename + ".log")
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
        if '+' in execname:
            execlist = execname.split("+")
            os.chmod("./" + execlist[0], stat.S_IRWXU)
            os.chmod("./" + execlist[1], stat.S_IRWXU)
            os.chmod("./" + execlist[2], stat.S_IRWXU)
            os.chmod("./" + execlist[3], stat.S_IRWXU)
        else:
            os.chmod("./" + execname, stat.S_IRWXU)  # 拥有者有全部权限(权限掩码)0o700
        return True
    except Exception as e:
        print(e)
        print("解压失败！")
        return False


def get_crash(crashname):  # 漏洞复现的时候使用
    data = [("name", crashname)]  # 依据crashname去数据库中获取该文件所在的路径，然后返回
    url = url_get_rep_crash + urllib.parse.urlencode(data)
    print(url)

    f = req.urlopen(url)
    data = f.read()
    with open(save_path + crashname, 'wb') as code:
        code.write(data)
    print("get crash success!")


def fuzz(fuzzer, execname, runtime, surplusum, jobname):
    input = save_path + "seeds"
    output = save_path + "crashs"
    info = save_path + "info/"
    target = save_path + execname  # 待测软件所在的路径
    logger.info(input)
    if fuzzer == "AFL":
        f2 = open(input + "/123", "w+")  # 往seeds目录中写入初始的种子文件
        f2.write("123")
        f2.close()

        aflfuzzer = afl.AflEngine()
        aflfuzzer.fuzz(input, output, info, target, afl_path, runtime, surplusum, nodename, execname)
        logger.info(jobname + " run out successfully")
        print("Afl run out successfully!")
    elif fuzzer == "AFLFAST":
        f2 = open(input + "/123", "w+")  # 往seeds目录中写入初始的种子文件
        f2.write("123")
        f2.close()

        aflfastfuzzer = aflfast.AFLFASTEngine()
        aflfastfuzzer.fuzz(input, output, info, target, aflfast_path, runtime, surplusum, nodename, execname)
        logger.info(jobname + " run out successfully")
        print("AFLFAST run out successfully!")
    elif fuzzer == "Libfuzz":
        libfuzz = libfuzzer.LibfuzzerEngine()
        libfuzz.fuzz(input, output, info, target, runtime, surplusum, nodename, execname)  # nodename全局变量
        # 前四个是执行模糊测试所必须的，nodename+surplusum用于标志日志名，execname用于结束进程
        logger.info(jobname + " run out successfully")
        print("Libfuzz run out successfully!")
    elif fuzzer == "Honggfuzz":
        f2 = open(input + "/123", "w+")  # 往seeds目录中写入初始的种子文件
        f2.write("123")
        f2.close()

        hongg = honggfuzz.HonggfuzzEngine()
        hongg.fuzz(input, output, info, target, hogngfuzz_path, runtime, surplusum, nodename, execname)
        logger.info(jobname + " run out successfully")
        print("Honggfuzz run out successfully!")


def reproduce(fuzzer, execname, jobname, crashname):
    target = save_path + execname
    crash_path = save_path + crashname
    if fuzzer == "AFL":
        aflfuzzer = afl.AflEngine()
        aflfuzzer.reproduce(target, crash_path, save_path)  # nodename全局变量
        print("Afl run out successfully!")

    elif fuzzer == "Libfuzz":
        libfuzz = libfuzzer.LibfuzzerEngine()
        libfuzz.reproduce(target, crash_path)  # nodename全局变量
        logger.info(jobname + " run out successfully")
        print("Libfuzz run out successfully!")

    elif fuzzer == "Honggfuzz":
        hongg = honggfuzz.HonggfuzzEngine()
        hongg.reproduce(target, crash_path)
        print("Honggfuzz run out successfully!")



# 依据不同的任务类型来完成不同的任务
def task_type(type, jobname, fuzzername, execname, runtime, surplusum, crashname):
    if type == "fuzz":
        # print("job: " + jobname + " is running!")
        logger.info("job: " + jobname + " is running!")
        fuzz(fuzzername, execname, runtime, surplusum, jobname)
    elif type == "reproduce":
        logger.info("reproduce: " + jobname + " is running!")
        reproduce(fuzzername, execname, jobname, crashname)
    else:
        print("Don't know the job type.")



def submit_crashes(jobname, fuzzer, execname):
    global crash_number  # 防止本地的crash命名冲突，每一轮任务完成后需要重置
    if fuzzer == "AFL":
        crash_path = save_path + "crashs/crashes/"
        target = save_path + execname
        aflfuzzer = afl.AflEngine()
        aflfuzzer.get_crash_info(crash_path, target, save_path)  # afl只产生漏洞测试用例，其对应的漏洞信息不会产生，所以这里需要生成漏洞对应的漏洞信息，便于定位
        crashlist = os.listdir(crash_path)
        print(crashlist)
        logger.info("submit crash")
        print(crashlist)

    elif fuzzer == "AFLFAST":
        crash_path = save_path + "crashs/crashes/"
        target = save_path + execname
        aflfastfuzzer = aflfast.AFLFASTEngine()
        aflfastfuzzer.get_crash_info(crash_path, target, save_path)  # afl只产生漏洞测试用例，其对应的漏洞信息不会产生，所以这里需要生成漏洞对应的漏洞信息，便于定位
        crashlist = os.listdir(crash_path)
        print(crashlist)
        logger.info("submit crash")
        print(crashlist)

    elif fuzzer == "Libfuzz":
        crash_path = save_path + "crashs/"
        crashlist = os.listdir(crash_path)
        print(crashlist)
        logger.info("submit crash")
        print(crashlist)

    elif fuzzer == "Honggfuzz":
        crash_path = save_path + "crashs/"
        submit_crashes_honggfuzz(crash_path, jobname)
        return

    else:
        print("Can't know the fuzzer type. (submit_crashes)")
        return

    for i in crashlist:  # 发送漏洞信息文件
        if i in crash_exist:
            continue
        if "info" in i or "README" in i:
            continue
        data = {"nodename": nodename, "jobname": jobname, "crashnum":\
                (jobname + "_" + nodename + "_" + "crash_" + str(crash_number))}
        res = requests.post(url_post_crash, files={"file": open(crash_path + i, 'rb')}, data=data)
        print("crash")
        print(res.text)
        # print(i)
        # print(crash_number)

        # for循环多余，有漏洞用例，必然会存在其对应的漏洞信息文件，所以直接发送即可
        for j in crashlist:  # 发送漏洞对应的漏洞信息文件
            if ("info" + i) == j:  # crashinfo的命名不能乱命名，info+漏洞信息名
                datainfo = {"nodename": nodename, "jobname": jobname, "crashnum": \
                            (jobname + "_" + nodename + "_" + "info_" + str(crash_number))}
                res1 = requests.post(url_post_crash, files={"file": open(crash_path + j, 'rb')}, data=datainfo)
                print("info")
                print(res1.text)
                break

        crash_exist[i] = crash_number
        crash_number = crash_number + 1


def submit_crashes_honggfuzz(crash_path, jobname):
    global crash_number  # 防止本地的crash命名冲突，每一轮任务完成后需要重置
    crashlist = os.listdir(crash_path)
    for i in crashlist:  # 发送漏洞信息文件
        if i in crash_exist:
            continue
        if "info" in i:
            continue
        data = {"nodename": nodename, "jobname": jobname, "crashnum":\
                (jobname + "_" + nodename + "_" + "crash_" + str(crash_number))}
        res = requests.post(url_post_crash, files={"file": open(crash_path + i, 'rb')}, data=data)
        print("crash")
        print(res.text)

        # 从HONGGFUZZ.REPORT.TXT中读取当前漏洞对应的漏洞信息
        loglist = os.listdir(save_path)
        for j in loglist:  # 遍历当前任务目录下的文件
            if j == "HONGGFUZZ.REPORT.TXT":
                f1 = open(save_path + "HONGGFUZZ.REPORT.TXT", "r")
                tem = f1.read()
                context = tem.split("TIME: ")
                flag = 0
                for k in context:  # 不同的漏洞信息块
                    m = k.split("\n")
                    for l in m:
                        if i in l:
                            f2 = open(crash_path + "info" + i, "ab")  # ab需要转码
                            f2.write(k.encode())
                            f2.close()

                            datainfo = {"nodename": nodename, "jobname": jobname, "crashnum": \
                                (jobname + "_" + nodename + "_info_" + str(crash_number))}
                            res1 = requests.post(url_post_crash, files={"file": open(crash_path + "info" + i, 'rb')},
                                                 data=datainfo)
                            print("info")
                            print(res1.text)

                            flag = 1
                            break
                    if flag == 1:
                        break
                break

        crash_exist[i] = crash_number
        crash_number = crash_number + 1



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



def submit_seeds(jobname, fuzzer):
    # seed_file_path = save_path + "/" + "seeds"
    global seed_number

    if fuzzer == "AFL":
        seed_path = save_path + "crashs/queue/"
    elif fuzzer == "AFLFAST":
        seed_path = save_path + "crashs/queue/"
    elif fuzzer == "Libfuzz":
        seed_path = save_path + "seeds/"
    elif fuzzer == "Honggfuzz":
        seed_path = save_path + "seeds/"
    else:
        print("Can't know the fuzzer type. (submit_seeds)" + fuzzer)
        return

    seedlist = os.listdir(seed_path)
    print("submit seeds")
    for i in seedlist:
        if i in seed_exist or i == ".state":
            continue
        try:
            data = {"nodename": nodename, "jobname": jobname, "seedhnum": (nodename + "_" + str(seed_number))}
            try:
                res = requests.post(url_post_seed, files={"file": open(seed_path + i, 'rb')}, data=data)
            except Exception as e:
                print(e)
            print(res.text)
            seed_exist[i] = seed_number
            seed_number = seed_number + 1
            # print(i)
            # print(seed_number)
        except Exception as e:
            print("submit_seeds() error: " + e)


def get_seeds(jobname, fuzzer):  # 第二步。种子同步阶段分两步走，先提交种子，在下载种子
    print("get_seeds")
    global seed_number

    if fuzzer == "AFL":
        seed_path = save_path + "crashs/queue/"
    elif fuzzer == "AFLFAST":
        seed_path = save_path + "crashs/queue/"
    elif fuzzer == "Libfuzz":
        seed_path = save_path + "seeds/"
    elif fuzzer == "Honggfuzz":
        seed_path = save_path + "seeds/"
    else:
        print("Can't know the fuzzer type. (get_seeds)")
        return

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
    seedlist = os.listdir(seed_path)  # 会从主节点将其他节点的种子全部下载下来，之后会依据本地种子队列中是否已经存在来决定是否添加
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
            shutil.move("./" + i, seed_path)
            seed_exist[i] = seed_number
            seed_number = seed_number + 1
        else:
            os.remove("./" + i)  # 目录重定向过了，定向到swap_seed中去了


def job_complete(jobname):
    data = {"jobname": jobname, "nodename": nodename}
    res = requests.post(url_post_jobcomplete, data=data)
    print(res.text)


def reproduce_complete(jobname, isfix, crashname):
    data = {"jobname": jobname, "nodename": nodename, "crashname": crashname, "isfix": isfix}
    res = requests.post(url_post_reproducecomplete, data=data)
    print(res.text)


if __name__ == '__main__':
    while(True):   # 子节点的管理脚本将一直运行
        # 获取任务
        job = get_job()  # job为字典类型
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
            res2 = get_crash(job["crashname"])
        elif job["type"] == "fuzz":
            res1 = get_archive("fuzz", job["name"], job["fuzzer"], job["exec"])

        # 开始fuzz
        runtime = 1
        surplusum = 1
        crashname = ''
        jobfuzzer = ""
        nowexec = ""
        if job["type"] == "fuzz":
            runtime = job["time"]  # if中的变量不可以在if外使用，除非在if之前已经对其进行声明了
            surplusum = job["surplusnum"]
            if job["fuzztype"] == 1:  # 前端传递给backend1的数据其类型均是str，而backend2传递给节点的数据则是按照数据库中各字段的类型
                jobfuzzer = job["fuzzer"]
                nowexec = job["exec"]
            elif job["fuzztype"] == 2:
                frs = job["fuzzer"].split("+")
                jobfuzzer = frs[surplusum-1]
                ers = job["exec"].split("+")
                nowexec = ers[surplusum-1]

        else:
            crashname = job["crashname"]

        print("thread start")
        logger.info("fuzz process start!")
        p1 = multiprocessing.Process(target=task_type, args=(job["type"], job["name"], jobfuzzer,\
                                 nowexec, runtime, surplusum, crashname))
        p1.start()
        # time.sleep(80)

        # fuzz类型的信息同步/上传漏洞复现结果
        if job["type"] == "fuzz":
            # if True:  # job["type"] == "fuzz"
            crash_number = 0  # 每一个任务运行时都会被重置
            crash_exist = {}
            seed_number = 0
            seed_exist = {}
            start_time = time.time()
            while time.time() - start_time < runtime + 3:
                time.sleep(time_sync)  # 每隔30秒同步一次，可以按需要设置
                submit_crashes(job["name"], jobfuzzer, nowexec)  # job["name"]
                submit_info(job["name"], job["surplusnum"])  # job["surplusnum"]
                submit_seeds(job["name"], jobfuzzer)
                get_seeds(job["name"], jobfuzzer)

            job_complete(job["name"])  # 时间一到，就会发送任务完成请求
        else:  # reproduce
            start_time = time.time()
            f_rep = 0
            while time.time() - start_time < 20:  # 20秒之内能检测完毕
                reproduce_file = save_path + "reproduce_result.txt"
                print(reproduce_file)
                if os.path.isfile(reproduce_file):  # reproduce已经完成
                    time.sleep(1)
                    f1 = open(reproduce_file, "r")
                    logger.info("reproduce_result.txt文件打开成功！")
                    tem = f1.read()
                    print("reproduce_result.txt文件内容")
                    print(tem)
                    context = tem.split("\n")
                    for j in context:
                        # print(j)
                        # if "========" in j:
                        if "=ERROR:" in j:
                            f_rep += 2  # 漏洞未修复
                            break
                    f_rep += 1  # 漏洞已修复
                if f_rep > 0:
                    break
                time.sleep(3)
            reproduce_complete(job["name"], f_rep, job["crashname"])

        print(job["name"] + " 已经完成！")



"""
线程是可以创建进程的，但是线程和他创建的进程之间没有继承关系，线程的资源是共享其所依附的进程的资源，
（线程只独立拥有很少一些自己运行所需要的资源），所以线程所创建的进程的父进程是线程所依附的进程，也可
将线程理解为他所依附的进程的一段代码。
"""
"""
https://www.cnblogs.com/qq991025/p/11783588.html 文件目录操作
https://blog.csdn.net/sinat_36188088/article/details/106410754 use request.post()
"""

