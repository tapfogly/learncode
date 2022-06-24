import pytest
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
    RBK.robot_config_uploadmap_req(mapPath = "testmap_1.smap")
    RBK.robot_control_loadmap_req(map_name = "testmap_1")
    RBK.robot_config_model_req(modelPath = "AMB-150.model")
    RBK.recoveryParam()


def test_1():
    """高级区域配置soundName为 lowBattery 时的测试用例
    """
    RBK.cancelTask()
    pos = {"x":-7.187, "y":3.161, "angle":0}
    RBK.moveRobot(pos)
    data = {"id":"LM4"}
    RBK.sendTask(data)
    while True:
        time.sleep(0.5)
        current_sname = json.loads(RBK.robot_status_sound_req()[1])["sound_name"]
        p = RBK.getPos()
        if p["x"] > -2.5:
            if current_sname != "lowBattery.wav":
                assert False, "sound name wrong {}".format(current_sname)
        ts = RBK.getTaskStatus()
        if ts["target_id"] == "LM4":
            status = ts["task_status"] 
            if status == 4:
                assert True
                break

def test_2():
    """高级区域配置soundName为 lowBattery 时，遇到障碍物，障碍物再被移开的测试用例
    """
    RBK.cancelTask()
    pos = {"x":-1.984, "y":0.294, "angle":0}
    RBK.moveRobot(pos)

    width = 0.5
    height = 0.5
    xmid = 0. # 动态障碍物的位置
    ymid = 3. # 动态障碍物的位置
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

    data = {"id":"LM3"}
    RBK.sendTask(data)
    while True:
        time.sleep(0.5)
        current_sname = json.loads(RBK.robot_status_sound_req()[1])["sound_name"]
        if current_sname == "block.wav":
            break
    RBK.robot_config_removeobstacle_req() # 移除动态障碍物

    while True:
        time.sleep(2.0)
        current_sname = json.loads(RBK.robot_status_sound_req()[1])["sound_name"]
        if current_sname == "block.wav":
            assert False, "sound name wrong {}".format(current_sname)
        if current_sname == "lowBattery.wav":
            assert True
            break  

if __name__ == "__main__":
    pytest.main(["-k test_2", "-v", "--html=report.html", "--self-contained-html"])