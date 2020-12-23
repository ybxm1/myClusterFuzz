#!/usr/bin/python
import engine
import subprocess
import psutil
import time

"""
Todo:
1. 读取日志信息的最后一行，将模糊测试的结果输出在屏幕上
"""

class AflEngine(engine.Engine):
  @property
  def name(self):
    return 'afl'

  def prepare(self, input_path, output_path, target_path):
    """
    准备模糊测试的执行命令
    """
    command = "./afl-2.52b/afl-fuzz " + " -i " + input_path + " -o " + output_path + " " + target_path
    return command

  def fuzz(self, start_cmd, max_time):
    """
    Todo: read the run_log and return the log information
    """
    # start_cmd = ["exec ./run.sh"]
    # print(start_cmd)
    t_start = time.time()
    pro = subprocess.Popen(start_cmd,  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in iter(pro.stdout.readline, ''):
      if len(i) < 1:
          break
      print(i.decode('utf-8').strip())
      if time.time() - t_start > max_time:
          break
    p = psutil.Process(pro.pid)
    p.terminate()
    for proc in psutil.process_iter():  # 通过进程名的方式来kill进程
        if proc.name() == "afl-fuzz":
            proc.terminate()
            print("afl-fuzz process end successfully!")
            break


  def reproduce(self, target_path, input_path, arguments, max_time):
    pass
    # os.chmod(target_path, 0o775)
    # runner = new_process.UnicodeProcessRunner(target_path)
    # with open(input_path) as f:
    #   result = runner.run_and_wait(timeout=max_time, stdin=f)
    #
    # return engine.ReproduceResult(result.command, result.return_code,
    #                               result.time_executed, result.output)



"""
参考链接：
1. subprocess.Popen介绍: https://blog.csdn.net/qq_34355232/article/details/87709418
"""