#!/usr/bin/python
import engine
import subprocess
import psutil
import time
import os
import shutil
import logging
from qsym import qsymuse  # 从qsym目录下导入qsymuse.py

"""
Todo:
1. 读取日志信息的最后一行，将模糊测试的结果输出在屏幕上
"""

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./log/qsym.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Start qsym log")

class Qsym():
  def name(self):
    return 'qsym'

  def fuzz(self, targetName, maindir):
      qsymuse.train(targetName, maindir)





