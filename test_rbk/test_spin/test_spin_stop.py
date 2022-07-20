# order_issue_pool#171  自动测试用例
# 使用注意： 目前需要手动上传地图和模型文件，以及将参数配置中的ObStopDist配置为0

import json
import sys
sys.path.append("../..")
from APILib.rbklib import rbklib, normalize_theta, getIP
import time
import pytest
import math

RBK = rbklib(ip = getIP())

def setup_module():
    RBK.lock()
    RBK.cancelTask()
    RBK.robot_config_uploadmap_req(mapPath = "spin_stop.smap")
    RBK.robot_control_loadmap_req(map_name = "spin_stop")
    RBK.robot_config_model_req(modelPath = "spin_stop.model")
    RBK.recoveryParam()

def waitCurrentTask():
    r = RBK
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break

def test_spin_stop():
    """ spin 电机卡住报错
    """ 
    r = RBK
    r.enableMotor("spin")

    time.sleep(0.5)
    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackUnload"
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    task_cmd = {
        "skill_name":"GoByOdometer",
        "robot_spin_angle":0.0,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    pos = {"x":-7.44, "y":-3.687, "angle":0.0}
    RBK.moveRobot(pos)

    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackLoad",
        "recfile":"shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    r.stopMotor("spin")
    time.sleep(1.0)

    task_cmd = {
        "id":"LM1"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    hasFail = False
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
        errs = json.loads(RBK.robot_status_alarm_req()[1])["errors"]
        if len(errs) > 0:
            hasFail = True
            break
    if hasFail:
        assert True
    else:
        assert False, "no error"


def test_spin_normal():
    """ spin 电机卡住报错
    """ 
    r = RBK
    r.enableMotor("spin")

    time.sleep(0.5)
    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackUnload"
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    task_cmd = {
        "skill_name":"GoByOdometer",
        "robot_spin_angle":0.0,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    pos = {"x":-7.44, "y":-3.687, "angle":0.0}
    RBK.moveRobot(pos)

    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackLoad",
        "recfile":"shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    task_cmd = {
        "skill_name":"GoByOdometer",
        "increase_spin_angle":1.57/2.0,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    waitCurrentTask()

    task_cmd = {
        "id":"LM1"
    }
    r.sendTask(task_cmd)
    time.sleep(1)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
        errs = json.loads(RBK.robot_status_alarm_req()[1])["errors"]
        if len(errs) > 0:
            assert False, "failed {}".format(errs.dumps())
            break
    assert True, "no error"

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])