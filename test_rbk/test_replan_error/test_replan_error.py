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

def test_replan():
    """
    https://seer-group.coding.net/p/robokit/requirements/issues/1212/detail
    导航过程中，中间点速度非0，暂停任务，推动车移开路径，再恢复任务，机器人到达中间点速度非0。
    """
    pos = {"x":-9.98,"y":11.5,"angle":90.0}
    RBK.moveRobot(pos) 
    data = {"id": "LM3"}
    RBK.sendTask(data) 
    while True:
        time.sleep(0.1)
        pos = RBK.getPos()
        RBK.robot_task_pause_req()
        break
    time.sleep(1)
    pos = {"x":0.1,"y":20.1,"angle":92.0}
    RBK.moveRobot(pos)
    RBK.robot_task_resume_req()    
if __name__ == "__main__":
    test_replan()