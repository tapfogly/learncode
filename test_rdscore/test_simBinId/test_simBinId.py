# order_issue_pool#400
import pytest
import time
import sys
sys.path.append("../..")
from APILib.orderLib import *


def test_simBinId(core):
    """
    发送id为库位名的任务
    """
    oid = core.gotoOrder(location="A008-1")
    time.sleep(2)
    o = core.orderDetails(orderId=oid)
    core.waitForOrderFinishTimeout(oid, 400)
    o = core.orderDetails(orderId=oid)
    assert o['state'] == "FINISHED"

v = "AMB-201"

def reset_pos(core):
    core.updateSimRobotState(json.dumps({"vehicle_id":v, "position_by_name":"LM217"}))
    time.sleep(2)

def test_simPause(core):
    """
    测试仿真机器人暂停
    """
    core.terminateAll(v)
    time.sleep(5)
    core.dispatchable(v)
    reset_pos(core)
    oid = core.gotoOrder(location="AP101", vehicle=v)
    time.sleep(2)
    o = core.orderDetails(orderId=oid)
    while o['state'] != "RUNNING":
        time.sleep(2)
        o = core.orderDetails(orderId=oid)

    core.gotoSitePause(v)
    time.sleep(10)
    o = core.robotStatus(v)

    assert o['rbk_report']['task_status'] == 3

    core.gotoSiteResume(v)
    core.waitForOrderFinishTimeout(oid, 200)
    o = core.orderDetails(oid)
    assert o['state'] == "FINISHED"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])