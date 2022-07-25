import pytest
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.orderLib import *

ORDER = OrderLib(getServerAddr())
ORDER.recoveryParam()

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "autoParkScene.zip")
    ORDER.uploadScene(p)
    time.sleep(30)

def init_pos(loc:str, name:str):
    ORDER.terminateAll(vehicle = name)
    ORDER.dispatchable(name = name)
    data = {
        "vehicle_id":name,
        "position_by_name": loc
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()
    time.sleep(1)

def test_autoPark1():
    """停靠中，立刻终止运行的运单
    """
    ORDER.recoveryParam()
    time.sleep(1)
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoPark":True,
        "StartParkTime":0.0
        }})
    init_pos(loc="AP13",name="sim_01")
    ORDER.terminateAll(vehicle = ["sim_01"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01"])
    time.sleep(2)
    o1 = ORDER.gotoOrder(vehicle="sim_01",location="AP18")
    time.sleep(0.1)
    ORDER.terminateId(order_id = o1)
    time.sleep(10)
    o2 = ORDER.getCurrentOrderId("sim_01")
    ORDER.waitForOrderFinish(uuid = o2)
    path = ORDER.robotStatus(vehicle_id = "sim_01")["area_resources_occupied"][0]["path_occupied"]
    has_ap22 = False
    for p in path:
        if p["end_id"] == "AP22":
            has_ap22 = True
            assert True
    if has_ap22 == False:
        assert False, str(path)

if __name__ == '__main__':
    pytest.main(["-v","--html=report.html", "--self-contained-html"])