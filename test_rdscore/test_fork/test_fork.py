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
    p = os.path.join(p, "rds_20220602140253.zip")
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
    time.sleep(10)
    
def test_self_position():
    '''
    重复下发同一个点，但是库位不同的订单
    '''
    init_pos("LM5", name = "SFL-01")
    order_id = ORDER.gotoOrder(location="DK-2-1-1", group="SFL", binTask = "load")
    ORDER.waitForOrderFinish(order_id)
    detail = ORDER.orderDetails(order_id)
    print(detail)
    order_id2 = ORDER.gotoOrder(location="DK-2-1-2", group="SFL", binTask = "load")
    gotoPreLM = False
    while True:
        time.sleep(0.5)
        r = ORDER.robotStatus(vehicle_id = "SFL-01")
        for a in r["area_resources_occupied"]:
            for p in a["path_occupied"]:
                if p["end_id"] == "LM5":
                    gotoPreLM = True
                    break
        if gotoPreLM:
            break
        detail = ORDER.orderDetails(order_id2)
        if detail["state"] == "FINISHED":
            break
    ORDER.waitForOrderFinish(order_id2)
    detail = ORDER.orderDetails(order_id2)
    if gotoPreLM and detail["state"] == "FINISHED":
        assert True
    else:
        assert False, "goto pre Lm {}, state {}".format(gotoPreLM, detail["state"])

def test_load_same_point():
    '''
    叉车初始位置就在终点，去终点的订单
    '''
    order_id = ORDER.gotoOrder(location="LM5", group="SFL")
    ORDER.waitForOrderFinish(order_id)
    detail = ORDER.orderDetails(order_id)
    init_pos("AP438", name = "SFL-01")
    order_id2 = ORDER.gotoOrder(location="DK-2-1-2", group="SFL", binTask = "load")
    gotoPreLM = False
    while True:
        time.sleep(0.5)
        r = ORDER.robotStatus(vehicle_id = "SFL-01")
        for a in r["area_resources_occupied"]:
            for p in a["path_occupied"]:
                if p["end_id"] == "LM5":
                    gotoPreLM = True
                    break
        if gotoPreLM:
            break
        detail = ORDER.orderDetails(order_id2)
        if detail["state"] == "FINISHED":
            break
    ORDER.waitForOrderFinish(order_id2)
    detail = ORDER.orderDetails(order_id2)
    if gotoPreLM and detail["state"] == "FINISHED":
        assert True
    else:
        assert False, "goto pre Lm {}, state {}".format(gotoPreLM, detail["state"])

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])