# https://seer-group.coding.net/p/robokit/bug-tracking/issues/645/detail 自动测试用例
# 使用注意： 目前需要手动上传地图和模型文件
# 这个自动化测试用例用于测试机器人平动


import json
import sys
sys.path.append("../..")
from APILib.rbklib import rbklib, normalize_theta, getIP
import time
import pytest
import math

def test_translate():
    """ 机器人平动测试"""
    
    r = rbklib(ip = "192.168.189.134")
    rpos = {"x":10.260, "y":4.017, "angle":0.} # agv初始化位置
    r.lock()
    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    r.moveRobot(rpos) # 让机器人在所在位置

    data = {"dist":5.0,"vx":1.0,"vy":0.0} # 平动设置{移动距离，x方向最大速度，y方向最大速度}
    r.translate(data=data)

    time.sleep(1.0)
    t0 = time.time()
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
        dt = time.time() - t0
        if dt > 10: # 任务持续时间
            r.cancelTask()
            assert False, "robot cannot move"
    assert True
if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])