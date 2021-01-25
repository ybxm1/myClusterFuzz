#!/usr/bin/python
import engine
import subprocess
import psutil
import time
import os
import shutil
import logging


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("./log/libfuzz.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Start libfuzz log")


class LibfuzzerEngine(engine.Engine):
  @property
  def name(self):
    return 'libfuzzer'

  def fuzz(self, input, output, info, target, runtime, surplusum, nodename, execname):
      info_path = info + nodename + "_" + str(surplusum) + ".log"  # 日志名是啥问题不大，但是要避免同一个节点多次运行日志的时候出现日志覆盖的问题
      # logger.info(info_path)
      cmd = (target + " " + input).split(" ")
      t_start = time.time()
      crashnum = 0
      # print(time.time() - t_start)
      # print(runtime)
      cycle = 1
      while time.time() - t_start < runtime:
          # print("第" + str(cycle) + "运行。")
          logger.info("第" + str(cycle) + "运行。")
          cycle += 1
          with open(info_path, "ab") as out:  # 追加，文件不存在就创建
              pro = subprocess.Popen(cmd, stderr=out)  # 异常对象无法在异常块作用域外访问
          while True:
              fp = subprocess.Popen.poll(pro)
              # print("查看进程是否结束")
              logger.info("查看进程是否结束")
              crashlog = "info"
              # print(fp)
              logger.info(fp)
              crashexist = 0
              if fp == 0 or fp == 1:  # libfuzz发现一个漏洞已经结束运行了
                  lsdir = os.listdir("./")
                  # print("发现一个漏洞")
                  logger.info("发现一个漏洞")
                  for i in lsdir:  # 将漏洞文件移入指定的目录中去
                      if "crash-" in i:
                          outputdir = os.listdir(output)  # 遍历output中的所有漏洞文件，如果新出现的漏洞文件名重合了，就抛弃
                          for k in outputdir:
                              if i == k:
                                  crashexist += 1
                                  break
                          if crashexist == 1:
                              print("漏洞" + i + "已存在。")
                              os.remove("./" + i)  # 删除当前目录下的crash文件
                              continue
                          shutil.move("./" + i, output)
                          crashlog += i  # 漏洞详细信息
                          # print(crashlog)
                          # print("漏洞移动成功")
                          logger.info(crashlog)
                          logger.info(i + "漏洞移动成功")

                  if crashexist == 1:
                      continue

                  # 从bot日志中读取漏洞对应的漏洞信息文件，并将其与漏洞存在一起
                  nowcrash = 0
                  flag = 0
                  f1 = open(info_path, "r")
                  # print("漏洞信息文件打开成功！")
                  logger.info("漏洞信息文件打开成功！")
                  tem = f1.read()
                  context = tem.split("\n")
                  for j in context:
                      # print(j)
                      if "========" in j:
                          if nowcrash == crashnum:
                              crashnum += 1
                              flag += 1
                              continue
                          else:
                              nowcrash += 1
                      if flag == 1:
                          f2 = open(output + "/" + crashlog, "ab")
                          f2.write((j + "\n").encode())
                          f2.close()
                  break
              elif time.time() - t_start > runtime:
                  break
              else:
                  time.sleep(5)

          if time.time() - t_start > runtime:
              # p = psutil.Process(pro.pid)
              # p.terminate()
              fp = subprocess.Popen.poll(pro)
              if fp == 0 or fp == 1 or fp == 2:
                  break
              for proc in psutil.process_iter():  # 通过进程名的方式来kill进程
                  if proc.name() == execname:  # 不同的模糊测试实例该名字不一样
                      proc.terminate()
                      print("libfuzz process end successfully!")
                      break
              break
      logger.info("任务完成！")



  def reproduce(self, target_path, crash_path):
      cmd = (target_path + " " + crash_path).split(" ")
      with open("./reproduce_result.txt", "ab") as out:  # 追加，文件不存在就创建
          pro = subprocess.Popen(cmd, stderr=out)  # 异常对象无法在异常块作用域外访问
      time.sleep(8)


"""
1. shell=True参数会让subprocess.Popen接受字符串类型的变量作为命令，并调用shell去执行这个字符串，当shell=False是，
subprocess.Popen只接受数组变量作为命令，并将数组的第一个元素作为命令，剩下的全部作为该命令的参数。 
2. >>>args = ['/bin/cat', '-input', 'test.txt', '-output', 'diege.txt', '-cmd', "echo '$MONEY'"]
   >>>p=subprocess.Popen(args)
3. subprocess:
      # fp = open(info_path, 'w')
      # fp.close()
      # os.chmod(info_path, 0o777)
      # fp = open(info_path, 'wb')
      # pro = subprocess.Popen(start_cmd, shell=True, stdout=fp)
      # pro = subprocess.Popen(cmd, shell=False, stdout=fp)
      # pro = subprocess.Popen(start_cmd, shell=True, stdout=subprocess.PIPE)  # stdout to screen
      # for i in iter(pro.stdout.readline, ''):
      #     if len(i) < 1:
      #         break
      #     res = i.decode('utf-8').strip()
      #     if time.time() - t_start > max_time:
      #         break
"""

"""
1. poll的返回值：　0正常结束, 1sleep, 2子进程不存在, none正在运行
"""

"""
问题：
1. 为什么这里创建进程的时候添加stderr就无法显示子进程的输出信息？
"""
