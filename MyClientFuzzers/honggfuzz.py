#!/usr/bin/python
#!/usr/bin/python
import engine
import subprocess
import psutil
import time

"""
Todo:
1. 读取日志信息的最后一行，将模糊测试的结果输出在屏幕上
"""

class HonggfuzzEngine(engine.Engine):
  @property
  def name(self):
    return 'honggfuzzer'

  def prepare(self, input_path, output_path, target_path, runtime):
    """
    准备模糊测试的执行命令
    """
    command = "./honggfuzz/honggfuzz " + " -i " + input_path + " -o " + output_path + \
              " --run_time " + runtime + " -- " + target_path + " ___FILE___"
    return command

  def fuzz(self, start_cmd):
    pro = subprocess.Popen(start_cmd,  shell=True, stdout=subprocess.PIPE)
    for i in iter(pro.stdout.readline, ''):
      if len(i) < 1:
          break
      print(i.decode('utf-8').strip())

    p = psutil.Process(pro.pid)
    p.terminate()
    # honggfuzz通过在start_cmd中设定运行时间后会自动结束，无需人为结束创建的子进程


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

"""