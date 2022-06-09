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
    time.sleep(5)


def test_simBinId():
    """
    发送id为库位名的任务
    """
    oid = ORDER.gotoOrder(location="A008-1")
    time.sleep(2)
    o = ORDER.orderDetails(orderId=oid)
    ORDER.waitForOrderFinishTimeout(oid, 200)
    o = ORDER.orderDetails(orderId=oid)
    assert o['state'] == "FINISHED"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])