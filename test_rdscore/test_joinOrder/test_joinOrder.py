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
    # p = os.path.abspath(__file__)
    # p = os.path.dirname(p)
    # p = os.path.join(p, "rds_join_order.zip")
    # ORDER.uploadScene(p)
    # time.sleep(30)

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

def test_charge_join_order():
    """一个车正在充电时，如果来一个运单
    https://seer-group.coding.net/p/order_issue_pool/bug-tracking/issues/826/detail
    """
    ORDER.recoveryParam()
    time.sleep(1)
    ORDER.modifyParam({"RDSDispatcher":{
        "AutoCharge":True,
        "AutoPark":False,
        "StartChargeTime": 0.0,
        "ClearDBOnStart": True,
        }})    
    init_pos(loc="AP8",name="HR-03")
    init_pos(loc="LM928",name="HR-04")
    ORDER.terminateAll(vehicle = ["HR-03", "HR-04"])
    time.sleep(2)
    ORDER.dispatchable(name =  ["HR-03", "HR-04"])
    data = {        
        "vehicle_id":"HR-03",
        "battery_percentage": 0.4,
        "locked":True
    }
    ORDER.updateSimRobotState(json.dumps(data))
    time.sleep(4)
    o1 = ORDER.simpleOrder(fromLoc = "PS-04-02-1", toLoc = "PB-01-01-2")
    o2 = ORDER.simpleOrder(fromLoc = "PS-04-02-2", toLoc ="PB-01-02-2")
    time.sleep(3)
    name1 = ORDER.orderDetails(orderId = o1)["vehicle"]
    name2 = ORDER.orderDetails(orderId = o2)["vehicle"]
    ORDER.terminateId(order_id = o1)
    ORDER.terminateId(order_id = o2)
    assert name1 == "HR-03" and name2 == "HR-03", "{},{}".format(name1, name2)


def test_no_charge_join_order():
    """没有订单时拼单"""
    ORDER.modifyParam({"RDSDispatcher": {
        "AutoCharge": False,
        "AutoPark": False,
        "StartChargeTime": 0.0,
        "ClearDBOnStart": True,
        "JoinableDist": 99,
    }})
    init_pos(loc="AP8", name="HR-03")
    init_pos(loc="LM928", name="HR-04")
    ORDER.terminateAll(vehicle=["HR-03", "HR-04"])
    time.sleep(2)
    ORDER.dispatchable(name=["HR-03", "HR-04"])
    data = {
        "vehicle_id": "HR-03",
        "battery_percentage": 0.4,
        "locked": True
    }
    # ORDER.updateSimRobotState(json.dumps(data))
    time.sleep(4)
    o1 = ORDER.simpleOrder(fromLoc="MS-04-20-1", toLoc="PB-01-01-2")
    o2 = ORDER.simpleOrder(fromLoc="MS-02-02-2", toLoc="PB-01-02-2")
    time.sleep(3)
    name1 = ORDER.orderDetails(orderId=o1)["vehicle"]
    name2 = ORDER.orderDetails(orderId=o2)["vehicle"]
    # ORDER.terminateId(order_id=o1)
    # ORDER.terminateId(order_id=o2)
    assert name1 == "HR-03" and name2 == "HR-03", "{},{}".format(name1, name2)

if __name__ == '__main__':
    test_charge_join_order()
    # pytest.main(["-v","--html=report.html", "--self-contained-html"])