import laserOmni1
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

def setup_module():
    RBK.lock()
    # RBK.robot_config_uploadmap_req(mapPath = "20220607165443819.smap")
    # time.sleep(10)
    RBK.robot_control_loadmap_req(map_name = "20220607165443819")
    RBK.robot_config_model_req(modelPath = "omni.model")
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
    pos = {"x":-10, "y":-3, "angle":30}
    RBK.moveRobot(pos)

def test_avoid1():
    RBK.lock()
    RBK.robot_config_removeobstacle_req("1")
    RBK.clearSimLaser()
    time.sleep(0.5)
    RBK.setSimLaser(laserOmni1.x, laserOmni1.y)
    pos = {"x":-10, "y":-3, "angle":30}
    RBK.moveRobot(pos)
    data = {"id": "LM1"}
    RBK.sendTask(data)
    flag = RBK.waitForTaskFinished(60)
    if flag:
        assert True
    else:
        assert False

def test_avoid2():
    RBK.lock()
    RBK.robot_config_removeobstacle_req("1")
    time.sleep(1)
    width = 0.5
    height = 0.5
    xmid = -3.66
    ymid = -2.95
    xmin, ymin = xmid - width/2.0, ymid - height/2.0
    xmax, ymax = xmid + width/2.0, ymid + height/2.0
    RBK.robot_config_addgobstacle_req(
        name = "1",
        x1 = xmin,
        y1 = ymax,
        x2 = xmin,
        y2 = ymin,
        x3 = xmax,
        y3 = ymin,
        x4 = xmax,
        y4 = ymax
    )
    time.sleep(0.2)
    pos = {"x":1.014, "y":-2.95, "angle":30}
    RBK.moveRobot(pos)
    data = {"id": "LM2"}
    RBK.sendTask(data)
    flag = RBK.waitForTaskFinished(60)
    if flag:
        assert True
    else:
        assert False
    data = {"id": "LM3"}
    RBK.sendTask(data)
    flag = RBK.waitForTaskFinished(60)
    if flag:
        assert True
    else:
        assert False

def test_avoid3():
    RBK.lock()
    RBK.robot_config_removeobstacle_req("1")
    time.sleep(1)
    width = 0.5
    height = 0.5
    xmid = -3.66
    ymid = -2.95
    xmin, ymin = xmid - width/2.0, ymid - height/2.0
    xmax, ymax = xmid + width/2.0, ymid + height/2.0
    RBK.robot_config_addgobstacle_req(
        name = "1",
        x1 = xmin,
        y1 = ymax,
        x2 = xmin,
        y2 = ymin,
        x3 = xmax,
        y3 = ymin,
        x4 = xmax,
        y4 = ymax
    )
    time.sleep(0.2)
    pos = {"x":1.014, "y":-2.95, "angle":30}
    RBK.moveRobot(pos)
    data = {"id": "LM2"}
    RBK.sendTask(data)
    while True:
        time.sleep(1)
        pos = RBK.getPos()
        if pos["x"] <  -3.3:
            RBK.cancelTask()
            break
    
    data = {"id": "LM3"}
    RBK.sendTask(data)
    flag = RBK.waitForTaskFinished(60)
    if flag:
        assert True
    else:
        assert False

if __name__ == "__main__":
    test_avoid1()
