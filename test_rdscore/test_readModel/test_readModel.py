# order_issue_pool#51 的测试用例
import json
import sys
sys.path.append("../..")
from APILib.orderLib import *
import time
from multiprocessing import freeze_support
import pytest

ORDER = OrderLib(getServerAddr())

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global ORDER
    ORDER.uploadScene("test_rdscore/test_readModel/rds_20220421170742.zip")
    time.sleep(5)

def teardown_module():
    """执行这个脚本的后的内容
    """
    pass

def test_readModel():
    """这个是 order_issue_pool#51 的测试用例
    """
    oid = ORDER.gotoOrder(vehicle="AMB-01",location="LM2", complete=True)
    time.sleep(2.0)
    o = ORDER.orderDetails(orderId=oid)
    if "errors" in o and len(o["errors"]) == 0:
        assert True
    else:
        assert False, "order has error. {}".format(json.dumps(o.get("errors", []), indent=1))

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
