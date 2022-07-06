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
    RBK.robot_config_uploadmap_req(mapPath = "test_1.smap")
    RBK.robot_control_loadmap_req(map_name = "test_1")
    RBK.robot_config_model_req(modelPath = "robot.model")
    RBK.recoveryParam()
    RBK.modifyParam({
                "MoveFactory": {
                    "ObsStopDist": 0,
                    "Load_ObsStopDist": 0,
                    "UnloadSpin": True
                }
            })

def test_spin1():
    """ 测试两个线路货物朝向不同，agv要停下来，旋转好货物朝向再走
    """
    r = RBK
    rpos = {"x":-2.158, "y":-1.679, "angle":90.} # agv初始化位置
    r.lock()
    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos ={"sim":{"setPos":rpos}}
    r.sendTask(pos) # 让机器人在所在位置
    r.moveLoc(rpos) # 让agv定位在相同位置
    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackLoad",
        "recfile":"shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
    task_cmd = {
        "skill_name":"GoByOdometer",
        "global_spin_angle":0,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break

    task_cmd = {
            "id": "AP1622"
        }
    r.sendTask(task_cmd) #发送任务
    while True:
        ts = r.getTaskStatus()
        if ts["target_id"] == "AP1622":
            status = ts["task_status"] 
            if status == 4:
                break
            vel = r.getVel()
            pos = r.getPos()
            goods_dir = normalize_theta(vel["spin"] + pos["angle"])
            print("goods_dir: ", goods_dir, vel["spin"], pos["angle"])
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi/2.0) > 0.1:
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
    assert True

def test_spin2():
    """测试两个线路货物朝向相同，agv不要停下来，旋转好货物朝向再走
    """
    r = RBK
    rpos = {"x":-2.158, "y":-1.679, "angle":90.} # agv初始化位置
    r.lock()
    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos ={"sim":{"setPos":rpos}}
    r.sendTask(pos) # 让机器人在所在位置
    r.moveLoc(rpos) # 让agv定位在相同位置
    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackLoad",
        "recfile":"shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
    task_cmd = {
        "skill_name":"GoByOdometer",
        "global_spin_angle":-1.57,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
    task_cmd = {
            "id": "AP1622"
        }
    r.sendTask(task_cmd) #发送任务
    time.sleep(1.0)
    first_in = True
    while True:
        ts = r.getTaskStatus()
        if ts["target_id"] == "AP1622":
            status = ts["task_status"] 
            if status == 4:
                break
            vel = r.getVel()
            pos = r.getPos()
            goods_dir = normalize_theta(vel["spin"] + pos["angle"])
            print("goods_dir: ", goods_dir, vel["spin"], pos["angle"])
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi/2.0) > 0.1:
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
            if first_in:
                first_in = False
                if vel["r_vx"] < 0.1:
                    r.cancelTask()
                    assert False, "stop at start during goto AP1622".format(vel["r_vx"])
    assert True

def test_spin3():
    """测试两个线路，没有指明货物方向，因此中间不需要停下来
    """
    r = RBK
    rpos = {"x":4.076, "y":-1.679, "angle":90.} # agv初始化位置
    r.lock()
    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos ={"sim":{"setPos":rpos}}
    r.sendTask(pos) # 让机器人在所在位置
    r.moveLoc(rpos) # 让agv定位在相同位置
    task_cmd = {
        "id":"SELF_POSITION",
        "operation":"JackLoad",
        "recfile":"shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
    task_cmd = {
        "skill_name":"GoByOdometer",
        "global_spin_angle":-1.57,
        "spin_direction":0,
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            break
    task_cmd = {
            "id": "LM1591"
        }
    r.sendTask(task_cmd) #发送任务
    time.sleep(1.0)
    first_in = True
    while True:
        ts = r.getTaskStatus()
        if ts["target_id"] == "LM1591":
            status = ts["task_status"] 
            if status == 4:
                break
            vel = r.getVel()
            pos = r.getPos()
            goods_dir = normalize_theta(vel["spin"] + pos["angle"])
            # print("goods_dir: ", goods_dir, vel["spin"], pos["angle"])
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi/2.0) > 0.1:
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
            if first_in:
                first_in = False
                if vel["r_vx"] < 0.1:
                    r.cancelTask()
                    assert False, "stop at start during goto AP1622".format(vel["r_vx"])
    assert True

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])