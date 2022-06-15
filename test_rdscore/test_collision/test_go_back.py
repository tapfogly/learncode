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

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "rds_20220615105707.zip")
    ORDER.uploadScene(p)
    time.sleep(5)

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
    
def test_go_back():
    '''
    往回走
    '''
    ORDER.terminateAll(vehicle = ["AMB-03", "AMB-07", "AMB-06"])
    time.sleep(5)
    ORDER.recoveryParam()
    time.sleep(1)
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoCharge":False,
        "AutoPark":False,
        "PlanDist":1.0,
        "PlanStep":0.2
        }})

    init_pos("LM259", "AMB-06")
    init_pos("LM263", "AMB-07")
    init_pos("LM115", "AMB-02")
    order_id1 = ORDER.gotoOrder(location="AP380",vehicle="AMB-06")
    order_id2 = ORDER.gotoOrder(location="AP381",vehicle="AMB-07")
    time.sleep(15)
    r = ORDER.robotStatus("AMB-06")
    y0 = r["rbk_report"]["y"]
    print("y0 = ", y0)
    ORDER.undispatchable_ignore("AMB-02", False)
    while True:
        time.sleep(0.5)
        r = ORDER.robotStatus("AMB-06")
        y = r["rbk_report"]["y"]
        if y > (y0+0.1):
            assert False, " AMB-06 go back {} {}".format(y, y0)
            break
        detail1 = ORDER.orderDetails(order_id1)
        detail2 = ORDER.orderDetails(order_id2)
        if detail1["state"] == "FINISHED" and detail2["state"] == "FINISHED":
            assert True
            break

if __name__ == "__main__":
    pytest.main(["-k test_go_back","-v", "--html=report.html", "--self-contained-html"])