# order_issue_pool#400
import pytest
import time
import sys
sys.path.append("../..")
from APILib.orderLib import *

ORDER = OrderLib(getServerAddr())


def setup_module():
    global ORDER
    ORDER.uploadScene("test_rdscore/test_simBinId/scene.zip")
    time.sleep(5)


def test_simBinId():
    """
    发送id为库位名的任务
    """
    oid = ORDER.gotoOrder(location="A008-1")
    time.sleep(2)
    o = ORDER.orderDetails(orderId=oid)
    ORDER.waitForOrderFinishTimeout(oid, 20)
    o = ORDER.orderDetails(orderId=oid)
    assert o['state'] == "FINISHED"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])