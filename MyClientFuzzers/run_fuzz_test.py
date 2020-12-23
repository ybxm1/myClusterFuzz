#!/usr/bin/python
import argparse
import sys
import afl
import libfuzzer
import honggfuzz

"""
1. 处理输入的模糊测试参数
"""
# start_cmd = ["afl/afl-fuzz -i testcase -o output ./afl_test"]
parser = argparse.ArgumentParser(description='接收模糊测试参数')
parser.add_argument("--fuzzer", dest="fuzzer", help='请选择模糊器')
parser.add_argument("--input", dest="input", help="请指定输入目录")
parser.add_argument("--output", dest="output", help="请指定输出目录")
parser.add_argument("--target", dest="target", help="请给出待测模块的路径")
parser.add_argument("--runtime", dest="runtime", help="请给出待测模块的路径")
parser.add_argument("--crash", dest="crash", help="请给出漏洞文件的路径(libfuzz)")
parser.add_argument("--log", dest="log", help="请给出需要输出的日志文件路径和名称(honggfuzz)")
args = parser.parse_args(sys.argv[1:])


"""
2. 挑选合适的模糊测试引擎对模块进行模糊测试
"""
if args.fuzzer == "afl":
    aflfuzzer = afl.AflEngine()
    cmd = aflfuzzer.prepare(args.input, args.output, args.target)
    aflfuzzer.fuzz(cmd, int(args.runtime))
    print("Afl run out successfully!")

elif args.fuzzer == "libfuzzer":
    if args.crash:  # 实现漏洞复现
        libfuzz = libfuzzer.LibfuzzerEngine()
        libfuzz.reproduce(args.target, args.crash)
        print("reproduce crash successfully!")
    else:  # 实现模糊测试
        libfuzz = libfuzzer.LibfuzzerEngine()
        cmd = libfuzz.prepare(args.input, args.target)
        libfuzz.fuzz(cmd, args.output, int(args.runtime))
        print("Libfuzz run out successfully!")

elif args.fuzzer == "honggfuzz":
    hongg = honggfuzz.HonggfuzzEngine()
    cmd = hongg.prepare(args.input, args.output, args.target, args.runtime)
    hongg.fuzz(cmd)
    print("Honggfuzz run out successfully!")

else:
    print(args.fuzzer + " is not support. Please choose another fuzzer!")




"""
1. afl命令：
python run_fuzz.py --fuzzer afl --input /home/ybxm/MyFuzzers/Projects/AflTest/testcase --output /home/ybxm/MyFuzzers/Projects/AflTest/output --target /home/ybxm/MyFuzzers/Projects/AflTest/afl_test --runtime 20
2. libfuzzer命令：
python run_fuzz.py --fuzzer libfuzzer --input Projects/LibFuzzerTest/seeds  --output Projects/LibFuzzerTest/output --target Projects/LibFuzzerTest/handshake-fuzzer --runtime 60
python run_fuzz.py --fuzzer libfuzzer --crash Projects/LibFuzzerTest/output/crash-4e157ef0f80e707b7a1caad680fc1789a2cc6c53  --target Projects/LibFuzzerTest/handshake-fuzzer
3. honggfuzzer命令：
python run_fuzz.py --fuzzer honggfuzz --input Projects/HonggfuzzTest/input --output Projects/HonggfuzzTest/output --target Projects/HonggfuzzTest/honggfuzz_test --runtime 30
"""




