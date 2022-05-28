# order_issue_pool#394 的测试用例
import json
import sys
sys.path.append("../..")
from APILib.orderLib import *
import time
from multiprocessing import freeze_support
import pytest

ORDER = OrderLib(getServerAddr())

def init_pos():
    ORDER.dispatchable(name = "AMB-01")
    time.sleep(1)
    ORDER.terminateAll(vehicle = "AMB-01")
    ORDER.dispatchable(name = "AMB-01")
    data = {
        "vehicle_id":"AMB-01",
        "position_by_name":"AP1"
    }
    ORDER.updateSimRobotState(json.dumps(data))
    time.sleep(2.0)

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
    rs = ORDER.robotsStatus()
    for e in rs["alarms"]["errors"]:
        if e["code"] == 52122:
            assert False, "failed. has error {}".format(e)
    assert True

def test_2():
    """ 测试能否正常运行
    """
    init_pos()
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP7", complete=True)
    while True:
        time.sleep(2.0)
        o1 = ORDER.orderDetails(orderId=oid1)
        print(o1)
        if "state" not in o1:
            continue
        if o1["state"] == "RUNNING":
            continue
        elif o1["state"]  == "FINISHED":
            assert True
            break
        else:
            assert False, "cannot work. order status is {}".format(o1["state"])

if __name__ == "__main__":
    pytest.main(["-k test_2", "-v", "--html=report.html", "--self-contained-html"])