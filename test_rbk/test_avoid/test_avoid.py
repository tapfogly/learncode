import laserData1
import laserData3
import laserLocal1
import laserLocal2
import laserRotate0
import laserRotate1
# import pytest
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.rbklib import *
import matplotlib.pyplot as plt

RBK = rbklib(getIP())
OVER_TIME = 30

def setup_module():
    RBK.lock()
    RBK.robot_config_uploadmap_req(mapPath = "aps-d2-saw.smap")
    RBK.robot_control_loadmap_req(map_name = "aps-d2-saw")
    RBK.robot_config_model_req(modelPath = "robot.model")
    RBK.recoveryParam()
    RBK.modifyParam({
                "MoveFactory": {
                    "ObsExpansion": 0.0,
                    "PathWidth": 4.0,
                    "FG_SmoothDistRatio":0.5,
                    "FG_RealTimeAvoid":True,
                    "FG_ObsDistPlus":3.0
                }
            })
    pos = {"x":10.782701, "y":2.4977, "angle":-86.07}
    RBK.moveRobot(pos)

def test_path():
    RBK.clearSimLaser()
    time.sleep(0.5)
    x = laserData1.x
    y = laserData1.y
    RBK.setSimLaser(x, y)
    pos = {"x":10.782701, "y":2.4977, "angle":-86.07}
    RBK.moveRobot(pos)
    data = {"id":"LM6"}
    RBK.sendTask(data)
    t0 = time.time()
    while True:
        time.sleep(0.5)
        dt = time.time() - t0
        if dt > OVER_TIME:
            assert False, " over time f{OVER_TIME}"
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            assert True, " task finished"
            break

def test_narrow_path():
    RBK.clearSimLaser()
    time.sleep(0.5)
    x = laserData3.x
    y = laserData3.y
    RBK.setSimLaser(x, y)
    pos = {"x":19.522, "y":4.0, "angle":179.734}
    RBK.moveRobot(pos)
    data = {"id":"AP17"}
    RBK.sendTask(data)
    t0 = time.time()
    while True:
        time.sleep(0.5)
        dt = time.time() - t0
        if dt > OVER_TIME:
            assert False, " over time f{OVER_TIME}"
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            assert True, " task finished"
            break

def test_local():
    RBK.clearSimLaser()
    time.sleep(0.5)
    RBK.setSimLaser(laserLocal1.x, laserLocal1.y)
    pos = {"x":19.78, "y":4.0, "angle":179.58}
    RBK.moveRobot(pos)
    data = {"id": "AP17"}
    RBK.sendTask(data)
    time.sleep(3)
    RBK.clearSimLaser()
    time.sleep(0.5)
    RBK.setSimLaser(laserLocal2.x, laserLocal2.y)
    time.sleep(5)
    RBK.clearSimLaser()
    time.sleep(0.5)
    RBK.setSimLaser(laserLocal1.x, laserLocal1.y)
    t0 = time.time()
    while True:
        time.sleep(0.5)
        dt = time.time() - t0
        if dt > OVER_TIME:
            assert False, " over time f{OVER_TIME}"
        ts = r.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            assert True, " task finished"
            break

def test_rotate():
    RBK.modifyParam({
        "MoveFactory": {
            "ObsExpansion": 0.05,
        }
    })
    RBK.clearSimLaser()
    time.sleep(0.5)
    # RBK.setSimLaser(laserRotate0.x, laserRotate0.y)
    RBK.setSimLaser(laserRotate1.x, laserRotate1.y)
    pos = {"x":12.473572,"y":4.34269,"angle":174.494668}
    RBK.moveRobot(pos)
    data = {"id": "LM5"}
    RBK.sendTask(data)
    t0 = time.time()
    while True:
        time.sleep(0.5)
        dt = time.time() - t0
        if dt > OVER_TIME:
            assert False, " over time f{OVER_TIME}"
        ts = RBK.getTaskStatus()
        status = ts["task_status"] 
        if status == 4:
            assert True, " task finished"
            break

if __name__ == "__main__":
    setup_module()
    test_rotate()
