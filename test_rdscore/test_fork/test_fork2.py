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
    p = os.path.join(p, "rds_20220613191346.zip")
    ORDER.uploadScene(p)
    time.sleep(5)

def init_pos(loc:str, name:str):
    ORDER.terminateAll(vehicle = name)
    ORDER.dispatchable(name = name)
    data = {
        "vehicle_id":name,
        "position_by_name": loc,
        "speed":0.3
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()
    time.sleep(3)
    
def test_omni_path_fork():
    '''
    单向线路上或者路径的规划
    '''
    init_pos("LM106", name = "AMB-01")
    order_id = ORDER.gotoOrder(location="PP101")
    while True:
        time.sleep(0.5)
        detail = ORDER.orderDetails(order_id)
        # print(detail)
        if detail["state"] == "FINISHED":
            assert True
            break
        detail2 = ORDER.robotsStatus()
        if len(detail2['alarms']['errors']) > 0:
            ORDER.terminateId(order_id)
            assert False, "has error {}".format(detail2['alarms']['errors'])

def test_one_path_fork():
    '''
    单向线路上或者路径的规划
    '''
    init_pos("LM115", name = "AMB-01")
    order_id = ORDER.gotoOrder(location="LM116")
    while True:
        time.sleep(0.5)
        detail = ORDER.orderDetails(order_id)
        # print(detail)
        if detail["state"] == "FINISHED":
            assert True
            break
        detail2 = ORDER.robotsStatus()
        if len(detail2['alarms']['errors']) > 0:
            ORDER.terminateId(order_id)
            assert False, "has error {}".format(detail2['alarms']['errors'])

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])