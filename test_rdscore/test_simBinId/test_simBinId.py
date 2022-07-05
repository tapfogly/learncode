# order_issue_pool#400
import pytest
import time
import sys
sys.path.append("../..")
from APILib.orderLib import *

ORDER = OrderLib(getServerAddr())


def setup_module():
    global ORDER
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "scene.zip")
    ORDER.uploadScene(p)
    ORDER.modifyParam({"RDSDispatcher":{"ClearDBOnStart":True}, "ClearOldOrdersDisabled":True})
    time.sleep(5)


def test_simBinId():
    """
    发送id为库位名的任务
    """
    oid = ORDER.gotoOrder(location="A008-1")
    time.sleep(2)
    o = ORDER.orderDetails(orderId=oid)
    ORDER.waitForOrderFinishTimeout(oid, 400)
    o = ORDER.orderDetails(orderId=oid)
    assert o['state'] == "FINISHED"

v = "AMB-201"
def reset_pos():
    ORDER.updateSimRobotState(json.dumps({"vehicle_id":v, "position_by_name":"LM217"}))
    time.sleep(2)

def test_simPause():
    """
    测试仿真机器人暂停
    """
    ORDER.terminateAll(v)
    time.sleep(5)
    ORDER.dispatchable(v)
    reset_pos()
    oid = ORDER.gotoOrder(location="AP101", vehicle=v)
    time.sleep(2)
    o = ORDER.orderDetails(orderId=oid)
    while o['state'] != "RUNNING":
        time.sleep(2)
        o = ORDER.orderDetails(orderId=oid)

    ORDER.gotoSitePause(v)
    time.sleep(10)
    o = ORDER.robotStatus(v)

    assert o['rbk_report']['task_status'] == 3

    ORDER.gotoSiteResume(v)
    ORDER.waitForOrderFinishTimeout(oid, 200)
    o = ORDER.orderDetails(oid)
    assert o['state'] == "FINISHED"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])