import time
import subprocess
import os


class docker:
    # 初始化docker类
    def __init__(self, imageName, args):
        self.imageName = imageName
        self.parameters = args
        self.fuzzSets = {}

    # 创建一个docker容器(root权限)
    def run(self):
        # 创建容器的参数
        s = 'docker run {mode} --name={dockerName} --cpus=1 --cpuset-cpus="{core}" --ipc="host" ' \
            '{permission} {user} {workdir} --volume {targetVolumeMapping} ' \
            '--volume {outputVolumeMapping} {fuzzerImageName} {shell} > /dev/null 2>&1'.format(
            mode=self.parameters['runMode'],
            dockerName=self.parameters['dockerName'],
            core=self.parameters['cpuNo'],
            permission=self.parameters['permission'],
            user=self.parameters['user'],
            workdir=self.parameters['workDir'],
            targetVolumeMapping=self.parameters['targetVolumeMapping'],
            outputVolumeMapping=self.parameters['outputVolumeMapping'],
            fuzzerImageName=self.imageName,
            shell=self.parameters['shell'])
        os.system(s)
        print(f"已创建容器{self.parameters['dockerName']}!", flush=True)

    # 删除创建出来的docker容器
    def stop(self):
        # 停止容器
        s1 = 'docker stop {dockerName} > /dev/null 2>&1'.format(dockerName=self.parameters['dockerName'])
        os.system(s1)
        # 删除容器
        s2 = 'docker rm {dockerName} > /dev/null 2>&1'.format(dockerName=self.parameters['dockerName'])
        os.system(s2)
        print(f"容器{self.parameters['dockerName']}已删除!", flush=True)

    # 在screen中执行命令qsym(打开两个会话)
    def execQsymInScreen(self, dockerCommand, qsymCommand):
        # 创建新的screen
        # screenCmd1 = ("screen -dmS {screenName} bash -c '{command}'".format(
        #     screenName=self.parameters['dockerName'], command=dockerCommand))
        screenCmd12 = ("screen -dmS {screenName}-2 bash -c '{command}'".format(
            screenName=self.parameters['dockerName'], command=dockerCommand))
        # os.system(screenCmd1)
        # 在新的screen中执行模糊测试
        # screenCmd2 = ("screen -r {screenName} -X stuff '{command}'".format(
        #     screenName=self.parameters['dockerName'], command=fuzzerCommand))
        screenCmd22 = ("screen -r {screenName}-2 -X stuff '{command}'".format(
            screenName=self.parameters['dockerName'], command=qsymCommand))
        # os.system(screenCmd2)
        # screenCmd3 = ("screen -r {screenName} -X stuff '\n'".format(
        #     screenName=self.parameters['dockerName']))
        screenCmd32 = ("screen -r {screenName}-2 -X stuff '\n'".format(
            screenName=self.parameters['dockerName']))
        # os.system(screenCmd3)
        # s = subprocess.run(f'{screenCmd1} && {screenCmd2} && {screenCmd3}', shell=True)
        s2 = subprocess.run(f'{screenCmd12} && {screenCmd22} && {screenCmd32}', shell=True)
        print(
            # f"模糊器{self.parameters['fuzzerName']}在screen：{self.parameters['dockerName']}和{self.parameters['dockerName']}-2上显示测试信息！",
            f"模糊器{self.parameters['fuzzerName']}在{self.parameters['dockerName']}-2上显示测试信息！",
            flush=True)

    # 根据选择的模糊器调用相应的函数
    def fuzz(self, args):
        self.fuzzSets = args
        choosenFunction = 'self.' + self.parameters['fuzzerName'] + 'Fuzz()'
        eval(choosenFunction)
        if 'h' in self.fuzzSets['timeToFuzz']:
            timeToSleep = int(self.fuzzSets['timeToFuzz'][:-1]) * 3600 + 60
        elif 'm' in self.fuzzSets['timeToFuzz']:
            timeToSleep = int(self.fuzzSets['timeToFuzz'][:-1]) * 60 + 60
        elif 's' in self.fuzzSets['timeToFuzz']:
            timeToSleep = int(self.fuzzSets['timeToFuzz'][:-1]) + 60
        time.sleep(timeToSleep)


    # 开始qsym的模糊测试
    def qsymFuzz(self):
        '''
        fuzzerCommand = "cd target/{targetDir}; " \
                        "AFL_NO_AFFINITY=1 timeout {timeToFuzz} {fuzzerAddress} -S {processName} -i {inputDir} " \
                        "-o {outputDir} -m none -t {timeOut} -- /root/workdir/target/{targetDir}/{target} @@ " \
            .format(
            targetDir=self.fuzzSets['targetSetName'] + '/' + self.fuzzSets['targetName'],
            timeToFuzz=self.fuzzSets['timeToFuzz'],
            fuzzerAddress="/root/afl-2.52b/afl-fuzz",
            processName=self.parameters['dockerName'],
            inputDir=self.fuzzSets['seedsDir'],
            outputDir=self.fuzzSets['outputDir'],
            timeOut=self.fuzzSets['timeOut'],
            target=self.fuzzSets['targetName'])
        '''
        qsymCommand = "sleep 20; " \
                      "timeout {timeToFuzz} python {qsymAddress} -a 'swap_seed' -o {outputDir} -n qsym " \
                      "-- /home/test/{target} @@ " \
            .format(
            # targetDir=self.fuzzSets['targetSetName'] + '/' + self.fuzzSets['targetName'],
            timeToFuzz=self.fuzzSets['timeToFuzz'],
            # fuzzerAddress="/root/afl-2.52b/afl-fuzz",
            qsymAddress="/workdir/qsym/bin/run_qsym_afl.py",
            processName=self.parameters['dockerName'],  # need to change
            outputDir=self.fuzzSets['outputDir'],
            target=self.fuzzSets['targetName'])
        dockerCommand = "docker exec {execMode} {dockerName} {shell}".format(execMode=self.parameters['execMode'],
                                                                             dockerName=self.parameters['dockerName'],
                                                                             shell=self.parameters['shell'])
        # self.execQsymInScreen(dockerCommand, fuzzerCommand, qsymCommand)
        self.execQsymInScreen(dockerCommand, qsymCommand)
