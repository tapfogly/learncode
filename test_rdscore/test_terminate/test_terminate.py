# order_issue_pool#394 的测试用例
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
    ORDER.uploadScene("test_rdscore/test_terminate/rds_20220528144107.zip")
    time.sleep(5)

def teardown_module():
    """执行这个脚本的后的内容
    """
    pass

def init_pos():
    ORDER.terminateAll(vehicle = "AMB-01")
    ORDER.dispatchable(name = "AMB-01")
    data = {
        "vehicle_id":"AMB-01",
        "position_by_name":"AP1"
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()

def test_1():
    """ 测试停止一个的运行的订单
    """
    init_pos()
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP7", complete=True)
    time.sleep(5.0)
    oid2 = ORDER.gotoOrder(vehicle="AMB-01",location="LM8", complete=True)
    time.sleep(0.1)
    ORDER.terminateId(order_id = oid1)
    time.sleep(0.5)
    o1 = ORDER.orderDetails(orderId = oid1)
    o2 = ORDER.orderDetails(orderId = oid2)
    amb_01 = ORDER.robotStatus("AMB-01")
    ORDER.terminateIdList(ids = [oid1, oid2])
    try:
        if o1["state"]  == "STOPPED"\
            and ( o2["state"] == "CREATED"  or o2["state"] == "TOBEDISPATCHED") \
                and amb_01["undispatchable_reason"]["dispatchable_status"] == 1\
                    and amb_01["dispatchable"] == False:
            assert True
        else:
            assert False, "status: {}, {}, {}, {}".format(o1["state"], o2["state"], 
            amb_01["undispatchable_reason"]["dispatchable_status"], amb_01["dispatchable"])
    except Exception as e:
        assert False, "except: {}".format(str(e))

def test_2():
    """ 测试停止一个的等待的订单
    """
    init_pos()
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="LM18", complete=True)
    time.sleep(5.0)
    oid2 = ORDER.gotoOrder(vehicle="AMB-01",location="AP17", complete=True)
    time.sleep(0.1)
    ORDER.terminateId(order_id = oid2)
    time.sleep(0.5)
    o1 = ORDER.orderDetails(orderId = oid1)
    o2 = ORDER.orderDetails(orderId = oid2)
    amb_01 = ORDER.robotStatus("AMB-01")
    ORDER.terminateIdList(ids = [oid1, oid2])
    try:
        if o1["state"]  == "RUNNING"\
            and o2["state"] == "STOPPED"\
                and amb_01["undispatchable_reason"]["dispatchable_status"] == 0\
                    and amb_01["dispatchable"] == True:
            assert True
        else:
            assert False, "status: {}, {}, {}, {}".format(o1["state"], o2["state"], 
            amb_01["undispatchable_reason"]["dispatchable_status"], amb_01["dispatchable"])
    except Exception as e:
        assert False, "except: {}".format(str(e))

def test_3():
    """ 测试停止一个等待的订单，并且 disable_vehicle
    """
    init_pos()
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="LM2", complete=True)
    time.sleep(5.0)
    oid2 = ORDER.gotoOrder(vehicle="AMB-01",location="LM3", complete=True)
    time.sleep(0.1)
    ORDER.terminateId(order_id = oid2, disableVehicle=True)
    time.sleep(0.5)
    o1 = ORDER.orderDetails(orderId = oid1)
    o2 = ORDER.orderDetails(orderId = oid2)
    amb_01 = ORDER.robotStatus("AMB-01")
    ORDER.terminateIdList(ids = [oid1, oid2])
    try:
        if o1["state"]  == "RUNNING"\
            and o2["state"] == "STOPPED"\
                and amb_01["undispatchable_reason"]["dispatchable_status"] == 1\
                    and amb_01["dispatchable"] == False:
            assert True
        else:
            assert False, "status: {}, {}, {}, {}".format(o1["state"], o2["state"], 
            amb_01["undispatchable_reason"]["dispatchable_status"], amb_01["dispatchable"])
    except Exception as e:
        assert False, "except: {}".format(str(e))

def test_4():
    """ 测试停止一个等待的订单，并且 不disable_vehicle
    """
    init_pos()
    time.sleep(1.0)
    oid1 = ORDER.gotoOrder(vehicle="AMB-01",location="LM4", complete=True)
    time.sleep(5.0)
    oid2 = ORDER.gotoOrder(vehicle="AMB-01",location="LM3", complete=True)
    time.sleep(0.1)
    ORDER.terminateId(order_id = oid2, disableVehicle=False)
    time.sleep(0.5)
    o1 = ORDER.orderDetails(orderId = oid1)
    o2 = ORDER.orderDetails(orderId = oid2)
    amb_01 = ORDER.robotStatus("AMB-01")
    try:
        if o1["state"]  == "RUNNING"\
            and o2["state"] == "STOPPED"\
                and amb_01["undispatchable_reason"]["dispatchable_status"] == 0\
                    and amb_01["dispatchable"] == True:
            assert True
        else:
            assert False, "status: {}, {}, {}, {}".format(o1["state"], o2["state"], 
            amb_01["undispatchable_reason"]["dispatchable_status"], amb_01["dispatchable"])
    except Exception as e:
        assert False, "except: {}".format(str(e))

def test_5():
    """测试车子处于不占用资源状态，清除当前车所有订单时，车子不需要位于不可解单状态
    """
    init_pos()
    ORDER.undispatchable_ignore("AMB-01", True)
    time.sleep(1.0)
    ORDER.terminateAll(vehicle="AMB-01")
    amb_01 = ORDER.robotStatus("AMB-01")
    try:
        status = amb_01["undispatchable_reason"]["dispatchable_status"]
        if status == 2:
            assert True
        elif status == 1 or status == 0:
            assert False, "status {} error!".format(status)
    except Exception as e:
        assert False, "except: {}".format(str(e))

if __name__ == "__main__":
    pytest.main(["-v", "-x", "-s", "--html=report.html", "--self-contained-html"])