# need change
# 模糊器容器的目标程序（待测二进制文件）的数据卷映射
# targetVolumeMapping = '/home/ybxm/myClusterFuzz/MyClientFuzzers/jobprojects/test/:/home/test/'
# 模糊器容器的结果数据卷映射
# outputVolumeMapping = '/home/ybxm/myClusterFuzz/MyClientFuzzers/jobprojects/test/:/home/test/'
# 创建的容器的运行模式
runMode = '-id'
execMode = '-it'
# 创建的容器的权限
permission = '--privileged=true'
# 创建的容器的默认用户
user = '--user=root'
# 创建的容器的工作目录
workDir = '--workdir=/root/workdir'
# 指定容器使用的shell
shell = '/bin/bash'
# 单个种子超时时长
timeOut = '1000+'
