import json
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.orderLib import *
import time
from multiprocessing import freeze_support
import pytest

ORDER = OrderLib(getServerAddr())

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global ORDER
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "rds_20220601210844.zip")
    print(p)
    ORDER.uploadScene(p)
    time.sleep(5)

def init_pos(loc:str):
    ORDER.terminateAll(vehicle = "AMB-01")
    ORDER.dispatchable(name = "AMB-01")
    data = {
        "vehicle_id":"AMB-01",
        "position_by_name": loc,
        "position_map":"SecondFloorMiddle_202201281718000",
        "speed":0.3
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()
    time.sleep(10)

def test_door():
    """过门时禁用门
    """
    init_pos("LM191")
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoPark":False
        }})
    o1 = ORDER.gotoOrder(vehicle="AMB-01", location="LM108")
    forbid_door = True
    # 测试禁用门是，机器人要暂停下来
    while True:
        time.sleep(1.0)
        status = ORDER.robotStatus("AMB-01")
        task_status = status["rbk_report"]["task_status"]
        print(task_status, forbid_door)
        if forbid_door == False and task_status !=3:
            assert False, "forbid door robot doesn't stop. state = {}".format(task_status)
        if task_status == 3:
            break
        if task_status == 2 and forbid_door:
            forbid_door = False
            ORDER.disableDoor(names = ["Door-01"], disabled = True)
            time.sleep(1.0)

    ORDER.disableDoor(names = ["Door-01"], disabled = False)
    # 测试恢复门，机器人继续行走
    while True:
        time.sleep(1.0)
        o1status = ORDER.orderDetails(orderId = o1)
        status = ORDER.robotStatus("AMB-01")
        task_status = status["rbk_report"]["task_status"]
        print(task_status, o1status["state"])
        if task_status !=2 and task_status !=4 :
            assert False, "robot status {} error after door is ok.".format(task_status)
        if o1status["state"] == "FINISHED":
            assert True
            break

def test_lift():
    """过电梯时禁用电梯
    """
    init_pos("LM102")
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoPark":False
        }})
    o1 = ORDER.gotoOrder(vehicle="AMB-01", location="LM44")
    forbid_lift = True
    # 测试禁用lift，机器人要暂停下来
    while True:
        time.sleep(1.0)
        status = ORDER.robotStatus("AMB-01")
        task_status = status["rbk_report"]["task_status"]
        print(task_status, forbid_lift)
        if forbid_lift == False and task_status !=3:
            assert False, "forbid door robot doesn't stop. state = {}".format(task_status)
        if task_status == 3:
            break
        if task_status == 2 and forbid_lift:
            forbid_lift = False
            ORDER.disableLift(names = ["Lift-01"], disabled = True)
            time.sleep(1.0)

    ORDER.disableLift(names = ["Lift-01"], disabled = False)
    # 测试恢复lift，机器人继续行走
    while True:
        time.sleep(1.0)
        o1status = ORDER.orderDetails(orderId = o1)
        status = ORDER.robotStatus("AMB-01")
        task_status = status["rbk_report"]["task_status"]
        print(task_status, o1status["state"])
        if task_status !=2 and task_status !=4 and task_status != 0 :
            assert False, "robot status {} error after door is ok.".format(task_status)
        if o1status["state"] == "FINISHED":
            assert True
            break



if __name__ == "__main__":
    pytest.main(["-v", "-x", "-s", "--html=report.html", "--self-contained-html"])