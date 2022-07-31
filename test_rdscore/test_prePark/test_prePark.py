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
    ORDER.uploadScene("test_rdscore/test_prePark/scene.zip")
    print("setup_module ...")
    time.sleep(5)

def test_1():
    """ 
    """
    setup_module()
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "ClearDBOnStart":True,
        "AutoPark":True,
        "PreParkPoint":True,
        "StartParkTime":5,
        }})
    ORDER.terminateAll(vehicle = ["sim_01","sim_02","sim_03", "sim_04", "sim_05"])
    ORDER.dispatchable(name = ["sim_01","sim_02","sim_03", "sim_04", "sim_05"])
    init_pos(loc = "AP36", name="sim_05")
    init_pos(loc = "PP46", name="sim_04")
    init_pos(loc = "LM54", name="sim_03")
    init_pos(loc = "LM53", name="sim_02")
    init_pos(loc = "LM52", name="sim_01")
    o2 = ORDER.gotoOrder(vehicle="sim_05",location="AP35")
    time.sleep(15)
    o3 = ORDER.gotoOrder(vehicle="sim_01",location="AP35")



if __name__ == "__main__":
    test_1()

