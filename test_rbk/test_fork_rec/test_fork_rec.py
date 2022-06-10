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

def test_fork_rec():
    RBK.lock()
    RBK.clearErrors()
    RBK.robot_task_cleartargetlist_req()
    close_di ={"sim":{"setDI":[{"id":1,"status":False}]}}
    RBK.sendTask(close_di)
    RBK.recoveryParam()
    pos = {"x":0.912, "y":10.278, "angle":-90.0}
    RBK.moveRobot(pos)
    task_cmd = [
        {
            "source_id":"LM43",
            "id": "LM42",
            "task_id": str(time.time()),
            "reach_angle": 3.1415
        }]
    RBK.sendTaskList(task_cmd)
    while True:
        time.sleep(1)
        ts = RBK.getTaskStatus()
        status = ts["task_status"]
        print(status)
        if status == 4:
            break
    task_cmd = [{
            "source_id":"LM42",
            "id": "09.02.03",
            "operation": "ForkLoad",
            "task_id": str(time.time())
            }]
    RBK.sendTaskList(task_cmd)
    while True:
        time.sleep(1)
        p = RBK.getPos()
        if p["x"] > 2.23:
            break
    open_di ={"sim":{"setDI":[{"id":1,"status":True}]}}
    RBK.sendTask(open_di)
if __name__ == "__main__":
    test_fork_rec()