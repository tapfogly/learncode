"""
测试需要添加该目录下的机器人模型和地图文件
"""

import json
import math
import sys

import pytest

sys.path.append("..")
from APILib.rbklib import *
import json
import time

def setup_module():
    open_ip = None
    model = None
    s_id = None
    task_position = None
    with open("config.json", "r") as f:
        body = json.loads(f.read())
        open_ip = body["ip"]
        model = body["model_name"]
        s_id = body["source_id"]
        task_position = body["id"]
    return open_ip, model, s_id, task_position


ip, model_name, source_id, task_position = setup_module()
r = rbklib(ip, push_flag=True)
r.robot_config_lock_req("test_robot")


def test_robot_task_go1():
    '''
    纯固定路径导航
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/asupc6
    '''

    d = {
        "source_id": source_id,
        "id": task_position,
        "task_id": "test_1"
    }
    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0

    start = time.time()
    while True:
        end = time.time()
        body = json.loads(r.pushData.get())
        if end - start >= 30:
            break
        elif body["task_status"] == 2:
            time.sleep(1)
            continue
        elif body["task_status"] == 4:
            break
    body = json.loads(r.pushData.get())
    assert body["current_station"] == task_position, "导航命令执行有误，站点不匹配"
    time.sleep(2)


def test_robot_turn():
    '''
    转动
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ck7o3v
    '''

    angle = 180
    rad = angle * math.pi / 180
    d = {
        "angle": rad,
        "vw": 0.3
    }

    old_rad = json.loads(r.pushData.get())["angle"]

    head, body = r.robot_task_turn_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    start = time.time()
    while True:
        end = time.time()
        body = json.loads(r.pushData.get())
        if end - start >= 20:
            break
        elif body["task_status"] == 2:
            time.sleep(1)
            continue
        elif body["task_status"] == 4:
            break
        elif body["task_status"] == 5:
            # 任务失败
            assert False
        elif body["task_status"] == 6:
            # 任务取消
            assert True
    new_rad = json.loads(r.pushData.get())["angle"]
    abs_angle = abs(new_rad - old_rad)
    if new_rad > math.pi:
        abs_angle = 2 * math.pi - abs_angle
    if rad > math.pi:
        abs_angle = 2 * math.pi - abs_angle
    assert -0.01 < abs_angle - rad < 0.01
    time.sleep(2)

def test_point_center():
    '''
    运动到点精度
    '''

    '''
    机器人运动到目标点
    '''
    d = {
        "source_id": task_position,
        "id": source_id,
        "task_id": "test_amb300"
    }

    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    '''
    查看机器人导航状态
    '''
    st_time = time.time()
    while True:
        body = json.loads(r.pushData.get())
        ed_time = time.time()
        assert body["ret_code"] == 0, f"{body['err_msg']}"
        if body["task_status"] == 2:
            # 执行任务中
            time.sleep(1)
        elif body["task_status"] == 4:
            break
        elif ed_time - st_time >= 20:
            # 任务超时
            assert False
        else:
            assert False

    '''
    获取机器人当前的位置信息
    '''
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x1, y1 = body["x"], body["y"]

    '''
    查询目标点信息
    '''
    head, body = r.robot_status_station()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x2, y2 = None, None
    for i in range(len(body["stations"])):

        if body["stations"][i]["id"] == source_id:
            x2 = body["stations"][i]["x"]
            y2 = body["stations"][i]["y"]

    assert 0.01 >= abs(x2 - x1) and 0.01 >= abs(y2 - y1)
    time.sleep(2)

def test_spin1():
    """ 测试两个线路货物朝向不同，agv要停下来，旋转好货物朝向再走
    """
    time.sleep(3)
    r.modifyParam({
        "MoveFactory": {
            "ObsStopDist": 0,
            "Load_ObsStopDist": 0,
            "UnloadSpin": True
        }
    })
    rpos = {"x": -2.158, "y": -1.679, "angle": 90.}  # agv初始化位置

    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos = {"sim": {"setPos": rpos}}
    r.sendTask(pos)  # 让机器人在所在位置
    r.moveLoc(rpos)  # 让agv定位在相同位置
    task_cmd = {
        "id": "SELF_POSITION",
        "operation": "JackLoad",
        "recfile": "shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"]
        if status == 4:
            break
    task_cmd = {
        "skill_name": "GoByOdometer",
        "global_spin_angle": 0,
        "spin_direction": 0,
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
    r.sendTask(task_cmd)  # 发送任务
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
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi / 2.0) > 0.1:
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
    assert True

def test_spin2():
    """测试两个线路货物朝向相同，agv不要停下来，旋转好货物朝向再走
    """
    rpos = {"x": -2.158, "y": -1.679, "angle": 90.}  # agv初始化位置

    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos = {"sim": {"setPos": rpos}}
    r.sendTask(pos)  # 让机器人在所在位置
    r.moveLoc(rpos)  # 让agv定位在相同位置
    task_cmd = {
        "id": "SELF_POSITION",
        "operation": "JackLoad",
        "recfile": "shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"]
        if status == 4:
            break
    task_cmd = {
        "skill_name": "GoByOdometer",
        "global_spin_angle": -1.57,
        "spin_direction": 0,
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
    r.sendTask(task_cmd)  # 发送任务
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
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi / 2.0) > 0.1:
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
    rpos = {"x": 4.076, "y": -1.679, "angle": 90.}  # agv初始化位置

    time.sleep(1.0)
    r.clearErrors()
    r.cancelTask()
    pos = {"sim": {"setPos": rpos}}
    r.sendTask(pos)  # 让机器人在所在位置
    r.moveLoc(rpos)  # 让agv定位在相同位置
    task_cmd = {
        "id": "SELF_POSITION",
        "operation": "JackLoad",
        "recfile": "shelf/s0002.shelf"
    }
    r.sendTask(task_cmd)
    time.sleep(1.0)
    while True:
        ts = r.getTaskStatus()
        status = ts["task_status"]
        if status == 4:
            break
    task_cmd = {
        "skill_name": "GoByOdometer",
        "global_spin_angle": -1.57,
        "spin_direction": 0,
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
    r.sendTask(task_cmd)  # 发送任务
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
            if vel["r_vx"] > 0.1 and math.fabs(goods_dir + math.pi / 2.0) > 0.1:
                r.cancelTask()
                assert False, "go with spin {}, {}".format(vel["r_vx"], goods_dir)
            if first_in:
                first_in = False
                if vel["r_vx"] < 0.1:
                    r.cancelTask()
                    assert False, "stop at start during goto AP1622".format(vel["r_vx"])
    assert True


"""=============================================================================
===============================子项目测试=========================================
============================================================================="""


def test_jack_height():
    '''
    检查顶升高度
    '''
    head, body = r.robot_status_model_req()
    device_type = json.loads(body)["deviceTypes"]
    # print(body["deviceTypes"])
    height = None
    for i in range(len(device_type)):
        if device_type[i]["name"] == "jack":
            param = device_type[i]["devices"]
            for k in range(len(param)):
                if param[k]["name"] == "jack":
                    device_param = param[k]["deviceParams"]
                    for j in range(len(device_param)):
                        if device_param[j]["key"] == "type":
                            com = device_param[j]["comboParam"]["childParams"]
                            for z in range(len(com)):
                                if com[z]["key"] == "byDO":
                                    param = com[z]["params"]
                                    for w in range(len(param)):
                                        if param[w]["key"] == "maxHeight":
                                            height = param[w]["doubleValue"]
    if height >= 0.06:
        print("高度超过0.06， 实际高度=", height)
        assert False
    else:
        assert True


def test_rssi():
    '''
    获取网络信息强度
    '''
    rssi_value = json.loads(r.pushData.get())["rssi"]
    dbm = rssi_value - 100
    assert dbm >= -65, "网络信号强度低于-65"




