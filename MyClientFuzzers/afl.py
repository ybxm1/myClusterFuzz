#!/usr/bin/python
import engine
import subprocess
import psutil
import time
import os
import shutil
import logging

"""
Todo:
1. 读取日志信息的最后一行，将模糊测试的结果输出在屏幕上
"""

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log/afl.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Start afl-derive log")

class AflEngine(engine.Engine):
  @property
  def name(self):
    return 'afl-derive'

  def fuzz(self, input, output, info, target, afl_path, runtime, surplusum, nodename, execname, fuzzername):
    info_path = info + nodename + "_" + str(surplusum) + ".log"  # 日志名是啥问题不大，但是要避免同一个节点多次运行日志的时候出现日志覆盖的问题
    start_cmd = ""
    if fuzzername == "Radamsa":
        start_cmd = start_cmd + afl_path + "-S slave -R -i " + input + " -o " + output + " -m none -- " + target + " @@"
    else:
        start_cmd = start_cmd + afl_path + "-S slave -i " + input + " -o " + output + " -m none -- " + target + " @@"
    print(start_cmd)
    t_start = time.time()
    # pro = subprocess.Popen(start_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # with open(output + "/log/afl_run.log", "w") as out:
    #     pro = subprocess.Popen(start_cmd, shell=True, stdout=out, stderr=out)
    pro = subprocess.Popen(start_cmd, shell=True)

    fp = subprocess.Popen.poll(pro)
    print("进程状态码：")
    print(fp)
    # with open(output + "/afl-run-info", "ab") as out:  # 追加，文件不存在就创建
    #     pro = subprocess.Popen(start_cmd.split(" "), stderr=out)  # 异常对象无法在异常块作用域外访问
    while time.time() - t_start < runtime:
        time.sleep(5)
        if os.path.exists(output + "/plot_data"):
            print(output + "/plot_data 文件已经存在")
        else:
            print("文件不存在")
        f1 = open(output + "/plot_data", "r")  # 读取afl output中的plot_data文件内的数据
        tem = f1.read()
        f2 = open(info_path, "w+")  # 将读取到的文件信息作为日志信息存入info目录中; 覆盖原有的内容
        f2.write(tem)
        f1.close()
        f2.close()


    # 运行时间耗尽时，结束模糊进程
    p = psutil.Process(pro.pid)  # kill模糊测试进程
    p.terminate()
    for proc in psutil.process_iter():  # 通过进程名的方式来kill进程
      if proc.name() == execname:  # 不同的模糊测试实例该名字不一样
        proc.terminate()
        print(fuzzername + " process end successfully!")
    logger.info("任务完成！")


  def get_crash_info(self, crash_path, target, job_path):
      crashlist = os.listdir(crash_path)
      logger.info("get_crash_info")
      print("get_crash_info")
      print(job_path)

      for i in crashlist:
          if "info" in i or "README" in i:  #　只测漏洞用例
              continue
          f = 0
          for j in crashlist:  #　漏洞信息已经获取到了
              if ("info" + i) == j:
                  f += 1
                  break
          if f == 1:  # 漏洞对应的信息已经存在
              continue
          try:
              cmd = (target + " < " + crash_path + i)
              logger.info("cmd: " + cmd)
              # print(cmd)
              # print(crash_path)
              os.chdir(job_path)  # 必须切换到可执行文件所在的目录下
              # print(os.getcwd())
              with open(crash_path + "info" + i, "ab") as out:  # 追加，文件不存在就创建
                  pro = subprocess.Popen(cmd, shell=True, stdout=out, stderr=out)  # 与libfuzz的使用方式不同，若不这么写，异常信息无法存入文件中
                  # pro = subprocess.Popen(cmd.split(" "), stderr=out)  # 异常对象无法在异常块作用域外访问
          except Exception as e:
              logger.info("get_crash_info error!")
              logger.info(e)

  def reproduce(self, target_path, crash_path, job_path):
      os.chdir(job_path)  # 必须切换到可执行文件所在的目录下
      cmd = (target_path + " < " + crash_path)
      with open("./reproduce_result.txt", "ab") as out:  # 追加，文件不存在就创建
          pro = subprocess.Popen(cmd, shell=True, stdout=out, stderr=out)
      time.sleep(8)




"""
参考链接：
1. subprocess.Popen介绍: https://blog.csdn.net/qq_34355232/article/details/87709418
"""

"""
<unknown> terminated 错误信息
Aborted
"""

"""
handshark-afl所检测出来的漏洞信息：
=================================================================
==29209==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 808 byte(s) in 1 object(s) allocated from:
    #0 0x4a92a0  (/home/ybxm/myClusterfuzzClinet/client1/jobprojects/AFL/1-21-rep-afl/handshake-afl+0x4a92a0)
    #1 0x634fc1  (/home/ybxm/myClusterfuzzClinet/client1/jobprojects/AFL/1-21-rep-afl/handshake-afl+0x634fc1)

Indirect leak of 1824 byte(s) in 7 object(s) allocated from:
    #0 0x4a92a0  (/home/ybxm/myClusterfuzzClinet/client1/jobprojects/AFL/1-21-rep-afl/handshake-afl+0x4a92a0)
    #1 0x634fc1  (/home/ybxm/myClusterfuzzClinet/client1/jobprojects/AFL/1-21-rep-afl/handshake-afl+0x634fc1)

SUMMARY: AddressSanitizer: 2632 byte(s) leaked in 8 allocation(s).
"""