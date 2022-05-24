# author: yang da

from multiprocessing import freeze_support
import re
import time
from contextlib import contextmanager
import orderLib as ol

USE_EXISTING_CORE = True
SDK_PATH = "C:\\projects\\RDSCore-SDK-v0.0.17.0\\RDSCore-SDK-20211118-v0.0.17.0"
IP = "http://localhost:8088"
WINDOWS_LOG_DIR = "C:\\.SeerRobotics\\rdscore\\diagnosis\\log"


# TODO 测试报告、用例注册
def test_case(case):
    def wrap(f):
        def wrapped_f():
            print(f'******** test {case}')
            test_result = "passed" if f() else "failed"
            print(f'******** {test_result} {case}')
            return test_result
        return wrapped_f
    return wrap


# TODO 步骤失败，整个用例失败
@contextmanager
def test_step(step):
    print(f'[开始] {step}')
    try:
        yield
    finally:
        print(f'[完成] {step}')


def start_core(use_existing_core):
    '''
    启动rdscore的特殊阶段
    '''
    def wrap(f):
        def wrapped_f():
            if not use_existing_core:
                with test_step("启动RDSCore"):
                    freeze_support()
                p1 = ol.runRDSCore(SDK_PATH)
                time.sleep(5)
            result = f()
            if not use_existing_core:
                p1.terminate()
            return result
        return wrapped_f
    return wrap


def step_gain_control(ip):
    with test_step("获取控制权"):
        ol.locked(ip)
        time.sleep(3)


def check_log_reversed(pattern, timeout=100, log_dir=WINDOWS_LOG_DIR):
    '''
    倒序从log中找目标输出
    '''
    pattern_found = False
    start_time = time.time()
    regex = re.compile(pattern)
    log_file = ol.getLeasetLog(log_dir)

    while(time.time() - start_time < timeout):
        time.sleep(5)
        with open(log_file) as f:
            lines = reversed(f.readlines())
            for line in lines:
                if regex.match(line):
                    print(line)
                    pattern_found = True
                    break

        if pattern_found:
            break
        print("remaining log scan time {:.1f}s".format(
            timeout - time.time()+start_time), end='\r')
    print(f'\npattern {pattern} {"found" if pattern_found else "not found"}')
    return pattern_found
