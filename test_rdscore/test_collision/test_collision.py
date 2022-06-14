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
    p = os.path.join(p, "rds_20220614141424.zip")
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
    
def test_collision():
    '''
    异常碰撞检测
    '''
    ORDER.terminateAll(vehicle = ["AMB-03", "AMB-07"])
    ORDER.recoveryParam()
    time.sleep(1)
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoCharge":False,
        "AutoPark":False,
        "PlanDist":1.0,
        "PlanStep":0.2
        }})

    init_pos("LM259", "AMB-03")
    init_pos("LM263", "AMB-07")
    order_id1 = ORDER.gotoOrder(location="PP4",vehicle="AMB-03")
    time.sleep(10)
    order_id2 = ORDER.gotoOrder(location="TE7-MAT-2", vehicle="AMB-07")
    while True:
        time.sleep(0.5)
        detail1 = ORDER.orderDetails(order_id1)
        detail2 = ORDER.orderDetails(order_id2)
        # print(detail)
        if detail1["state"] == "FINISHED" and detail2["state"] == "FINISHED":
            assert True
            break
        rs = ORDER.robotsStatus()
        if len(rs['alarms']['errors']) > 0:
            if "AMB-07: blocked" in rs['alarms']['errors'][0]['desc']:
                assert False, "has error {}".format(rs['alarms']['errors'][0]['desc'])
                break

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])