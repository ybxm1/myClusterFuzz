import os
from multiprocessing.managers import BaseManager
import math
import threading

# 设置读取可用CPU列表的同步锁
cpuSetLocker = threading.Semaphore(1)


# CPU管理类（包括记录可用CPU编号、分配CPU、显示使用情况等）
class CpuManager:
    # 设置最大可占用的CPU数量为线程数的3/4，并记录CPU的使用状态字典
    def __init__(self):
        self.max_cpu = os.cpu_count()
        self.max_cpu_to_use = 1 # math.floor((self.max_cpu * 3) / 4)
        self.cpu_list = {}
        for i in range(self.max_cpu_to_use):
            self.cpu_list[i] = True
        self.free_cpu = threading.Semaphore(self.max_cpu_to_use)

    # 分配可用CPU的编号（还没有真正绑定CPU）
    def setCpu(self):
        self.free_cpu.acquire()
        cpuSetLocker.acquire()
        for key, value in self.cpu_list.items():
            if value:
                self.cpu_list[key] = False
                cpuSetLocker.release()
                return key

    # 回收已空闲的CPU的编号
    def freeCpu(self, cpuNo):
        cpuSetLocker.acquire()
        self.cpu_list[cpuNo] = True
        self.free_cpu.release()
        cpuSetLocker.release()

    # 打印所用本程序可用的CPU的使用情况
    def printCpuUsages(self):
        for key, value in self.cpu_list.items():
            # 使用参数flush=True，立即输出print的内容
            print(f'CPU {key} 是否可以使用：{value}', flush=True)

    # 用于多线程时返回分配的CPU编号
    def returnCpu(self, q):
        q.put(self.setCpu())


# 使用manager创建管理CPU的类的实例，使其可以在多进程间共享
def createCpuManger():
    manager = BaseManager()
    manager.register('CpuManager', CpuManager)
    manager.start()
    cpuManager = manager.CpuManager()
    return cpuManager


# 为进程绑定CPU，并将其优先级设置为最高
def bindCpu(pid, cpuNo):
    # 设置子进程可用的CPU编号
    os.sched_setaffinity(pid, {cpuNo})
    # 将该进程的优先级设置为最高(SCHED_FIFO策略为实时调度策略，没有时间片)
    max = os.sched_get_priority_max(os.SCHED_FIFO)
    p = os.sched_param(max)
    os.sched_setscheduler(pid, os.SCHED_FIFO, p)

