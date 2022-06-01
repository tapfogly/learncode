# order_issue_pool#394 的测试用例
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

def init_pos():
    ORDER.terminateAll(vehicle = "AMB-01")
    ORDER.dispatchable(name = "AMB-01")
    data = {
        "vehicle_id":"AMB-01",
        "position_by_name":"AP1"
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global ORDER
    ORDER.uploadScene("test_rdscore/test_repeatedLM/rds_20220528144107.zip")
    print("setup_module ...")
    time.sleep(5)

def teardown_module():
    """执行这个脚本的后的内容
    """
    print("teardown_module ...")


def test_1():
    """ 检查是否有52122的报错
    """
    init_pos()
    rs = ORDER.robotsStatus()
    for e in rs["alarms"]["errors"]:
        if e["code"] == 52122:
            assert False, "failed. has error {}".format(e)
    assert True

def test_2():
    """ 测试能否正常运行
    """
    init_pos()
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "G-MAPF":True,
        "G-MAPF-Vision":35,
        }})
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP7", complete=True)
    start_t = time.time()
    while True:
        time.sleep(2.0)
        o1 = ORDER.orderDetails(orderId=oid1)
        dt = time.time() - start_t
        if dt > 120:
            ORDER.terminateId(order_id=oid1)
            assert False, "time out 120s. order status is {}".format(o1["state"])
        if "state" not in o1:
            continue
        if o1["state"] == "RUNNING" or o1["state"] == "CREATED":
            continue
        elif o1["state"]  == "FINISHED":
            assert True
            break
        else:
            assert False, "cannot work. order status is {}".format(o1["state"])

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])