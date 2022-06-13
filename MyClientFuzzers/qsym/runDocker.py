import multiprocessing
import time
import os
import parameterSetup as set
from cpuManage import bindCpu
from dockerManage import docker


# 根据模糊器的名称启动docker，并调用相应模糊器的测试函数
def startDocker(cpuManger, fuzzerName, targetName, seedsDir, outputDir, timeToFuzz, maindir):
    # 获取空闲CPU
    cpuNo = cpuManger.setCpu()
    # 为进程绑定CPU，并将其优先级设置为最高(几乎可以独占这个CPU)
    bindCpu(pid=0, cpuNo=cpuNo)

    # 创建模糊器的容器
    # 获取模糊器的镜像名称
    imageName = "qsym/afl:2.52b"

    # 设置创建容器的参数
    parameters = {}
    # 设置创建的容器的运行模式
    parameters['runMode'] = set.runMode
    parameters['execMode'] = set.execMode
    # 设置容器的名称
    parameters['fuzzerName'] = fuzzerName
    parameters['dockerName'] = fuzzerName + '-' + str(os.getpid())
    # 设置使用的CPU编号
    parameters['cpuNo'] = cpuNo
    # 设置docker的运行权限
    parameters['permission'] = set.permission
    # 设置使用的用户和工作目录
    parameters['user'] = set.user
    parameters['workDir'] = set.workDir
    # 设置数据卷的映射
    parameters['targetVolumeMapping'] = maindir + ':/home/test/'  # 对应任务目录
    parameters['outputVolumeMapping'] = maindir + ':/home/test/'
    # 设置使用的shell
    parameters['shell'] = set.shell

    # 初始化docker类
    fuzzer = docker(imageName, parameters)  # dockerManage

    # 创建模糊器容器
    fuzzer.run()

    # 设置模糊测试的参数
    fuzzSets = {}
    # 设置模糊测试的对象名称
    fuzzSets['targetName'] = targetName
    # 设置模糊测试对象属于的测试集的名称
    # fuzzSets['targetSetName'] = targetInfo[1]
    # 设置模糊测试的时间
    fuzzSets['timeToFuzz'] = timeToFuzz
    # 设置种子文件夹
    fuzzSets['seedsDir'] = seedsDir
    # 设置单个种子的超时时间
    fuzzSets['timeOut'] = set.timeOut
    # 设置结果文件夹
    fuzzSets['outputDir'] = outputDir

    # 执行模糊测试
    p = multiprocessing.Process(target=fuzzer.fuzz(fuzzSets), args=())
    p.start()

    # 等待测试完成
    p.join()

    # 删除容器
    fuzzer.stop()

    time.sleep(2)

    # 释放绑定的CPU
    print(f'释放{cpuNo}号CPU')
    cpuManger.freeCpu(cpuNo=cpuNo)
