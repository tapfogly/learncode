# https://seer-group.coding.net/p/order_issue_pool/bug-tracking/issues/392/detail 自动测试用例
# 使用注意： 目前需要手动上传地图和模型文件
# 这个自动化测试用例用于测试，速度规划。当机器人有速度死区，速度规划已经能够让机器人正常运行


import json
import sys
sys.path.append("../..")
from APILib.rbklib import rbklib, normalize_theta, getIP
import time
import pytest
import math

def test_small():
    """ 机器人有速度死区，速度规划已经能够让机器人正常运行
    """
    r = rbklib(ip = getIP())
    rpos = {"x":-12.178, "y":-3.183, "angle":0.} # agv初始化位置
    r.lock()
    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    r.moveRobot(rpos) # 让机器人在所在位置

    data = {"RBKSim":{"RBKSimMinVx":0.1}}
    r.modifyParam(data = data)

    task_cmd = {
        "id":"LM1614"
    }

    r.sendTask(task_cmd)
    time.sleep(1.0)
    t0 = time.time()
    while True:
        ts = r.getTaskStatus()
        if ts["target_id"] == "LM1614":
            status = ts["task_status"] 
            if status == 4:
                break
            dt = time.time() - t0
            if dt > 10: # 任务持续时间
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
    assert True
if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])