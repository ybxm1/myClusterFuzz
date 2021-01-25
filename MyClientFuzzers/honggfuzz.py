#!/usr/bin/python
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
handler = logging.FileHandler("./log/honggfuzz.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Start honggfuzz log")

class HonggfuzzEngine(engine.Engine):
  @property
  def name(self):
    return 'honggfuzzer'


  def fuzz(self, input, output, info, target, honggfuzz_path, runtime, surplusum, nodename, execname):
    info_path = info + nodename + "_" + str(surplusum) + ".log"  # 日志名是啥问题不大，但是要避免同一个节点多次运行日志的时候出现日志覆盖的问题
    start_cmd = honggfuzz_path + " -i " + input + " -o " + input + " -l " + info_path + " --crashdir " + output + " -P " +\
                " --run_time " + str(runtime) + " -- " + target + " ___FILE___"
    print(start_cmd)
    # t_start = time.time()

    pro = subprocess.Popen(start_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fp = subprocess.Popen.poll(pro)
    print("进程状态码：")
    print(fp)
    time.sleep(runtime)

    # 运行时间耗尽时，结束模糊进程
    p = psutil.Process(pro.pid)  # kill模糊测试进程
    p.terminate()
    for proc in psutil.process_iter():  # 通过进程名的方式来kill进程
      if proc.name() == execname:  # 不同的模糊测试实例该名字不一样
        proc.terminate()
        print("honggfuzz process end successfully!")
    logger.info("任务完成！")

    # pro = subprocess.Popen(start_cmd,  shell=True, stdout=subprocess.PIPE)
    # for i in iter(pro.stdout.readline, ''):
    #   if len(i) < 1:
    #       break
    #   print(i.decode('utf-8').strip())
    # p = psutil.Process(pro.pid)
    # p.terminate()
    # honggfuzz通过在start_cmd中设定运行时间后会自动结束，无需人为结束创建的子进程


  def reproduce(self, target_path, crash_path):
      cmd = (target_path + " " + crash_path).split(" ")
      with open("./reproduce_result.txt", "ab") as out:  # 追加，文件不存在就创建
        pro = subprocess.Popen(cmd, stderr=out)  # 异常对象无法在异常块作用域外访问
      time.sleep(8)
    # os.chmod(target_path, 0o775)
    # runner = new_process.UnicodeProcessRunner(target_path)
    # with open(input_path) as f:
    #   result = runner.run_and_wait(timeout=max_time, stdin=f)
    #
    # return engine.ReproduceResult(result.command, result.return_code,
    #                               result.time_executed, result.output)



"""

"""