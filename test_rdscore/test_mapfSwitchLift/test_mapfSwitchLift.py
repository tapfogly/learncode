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

def init_pos(loc:str, name:str, a:float = 0.0):
    ORDER.terminateAll(vehicle = name)
    ORDER.dispatchable(name = name)
    data = {
        "vehicle_id":name,
        "position_by_name": loc,
        "angle": a
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()
    time.sleep(1)

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global ORDER
    ORDER.uploadScene("test_rdscore/test_mapfSwitchLift/scene.zip")
    print("setup_module ...")
    time.sleep(5)

def test_1():
    """ MAPF 通过电梯的互换位置
    """
    setup_module()
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "ClearDBOnStart":True,
        "AutoPark":False,
        "G-MAPF":True,
        "G-MAPF-MovablePark":True,
        }})
    ORDER.terminateAll(vehicle = ["AMB-03", "AMB-04"])
    time.sleep(2)
    init_pos(loc = "LM176", name="AMB-04")
    init_pos(loc = "LM69", name="AMB-03")
    ORDER.dispatchable(name = ["AMB-03", "AMB-04"])
    o2 = ORDER.gotoOrder(vehicle="AMB-04",location="LM69")
    time.sleep(1)
    o1 = ORDER.gotoOrder(vehicle="AMB-03",location="LM176")


if __name__ == "__main__":
    test_1()

