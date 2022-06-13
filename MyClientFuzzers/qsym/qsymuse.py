import multiprocessing
import time
from cpuManage import createCpuManger
from runDocker import startDocker

# 目标程序地址(“/root/workdir/target/”后的地址，即文件夹的名称，不包含文件名）
# targetDict = {"name1":"dir1",}  
# targetDict = {"name1":"cflow"}  # need change

# 使用预训练产生的种子对待测软件进行训练
def train(targetName, maindir):
    # targetNeedToRun = dict((key, value) for key, value in targetDict.items() if key in trainTargetList)
    # 种子文件夹位置
    docker_seedsDir = "/home/test/output/"  # qsym 使用时无用，只用于afl测试时
    # 输出文件夹位置  ### change
    docker_outputDir = "/home/test/output/"  # docker镜像中的位置
    # 测试时长(例如“1h”，“30m“)  ### change
    timeToFuzz = "5m"
    # 每个待测软件的测试次数  
    repeatTimes = 1

    # 创建的模糊器子进程列表
    processList = []
    # 创建模糊器子进程
    # for target in targetNeedToRun.items():
    # 设置使用的模糊器
    fuzzerName = "qsym"
    # 设置目前测试的轮次
    for num in range(repeatTimes):
        # 设置每个待测程序对应的输出文件夹
        # thisOutputDir = outputDir + target[0] + '-' + fuzzerName + '-' + str(num)
        p = multiprocessing.Process(target=startDocker,
                                    args=(createCpuManger(), fuzzerName, targetName, docker_seedsDir, docker_outputDir, timeToFuzz, maindir))
        processList.append(p)
        p.start()
        time.sleep(1)

    # 等待所有模糊器都执行完毕
    for p in processList:
        p.join()

    time.sleep(2)
    print(f'测试完毕！')

# #  need change
# if __name__ == '__main__':
#     cpuManger = createCpuManger()
#     # 填写测试集中的软件名的列表
#     #　trainTargetList = ["name1"]  ### change
#     train(targetName="cflow", cpuManger=cpuManger)
