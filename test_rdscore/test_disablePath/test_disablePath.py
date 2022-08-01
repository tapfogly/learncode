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
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "test_disablePath.zip")
    ORDER.uploadScene(p)
    time.sleep(30)

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

def test_disablePoint():
    """禁用点位，并且启用点位
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    init_pos(loc="AP15",name="sim_02")
    ORDER.terminateAll(vehicle = ["sim_01", "sim_02", "sim_03"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01", "sim_02", "sim_03"])
    ORDER.disablePoint(name = "LM59")
    o1 = ORDER.gotoOrder(vehicle="sim_02",location="AP18")
    time.sleep(10)
    ORDER.enablePoint(name = "LM59")
    assert ORDER.isOrderFinished(uuid = o1, timeout=30)

def test_disablePoint2():
    """禁用点位，绕行
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    init_pos(loc="AP15",name="sim_02")
    ORDER.terminateAll(vehicle = ["sim_01", "sim_02", "sim_03"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01", "sim_02", "sim_03"])
    ORDER.disablePoint(name = "LM57")
    o1 = ORDER.gotoOrder(vehicle="sim_02",location="AP18")
    assert ORDER.isOrderFinished(uuid = o1, timeout=60)

def test_disablePath():
    """禁用线路，并且启用线路
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    init_pos(loc="AP15",name="sim_02")
    ORDER.terminateAll(vehicle = ["sim_01", "sim_02", "sim_03"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01", "sim_02", "sim_03"])
    ORDER.disablePath(name = "LM59-AP18")
    o1 = ORDER.gotoOrder(vehicle="sim_02",location="AP18")
    time.sleep(10)
    ORDER.enablePath(name = "LM59-AP18")
    assert ORDER.isOrderFinished(uuid = o1, timeout=30)

def test_disablePath2():
    """禁用线路绕行
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    init_pos(loc="AP15",name="sim_02")
    ORDER.terminateAll(vehicle = ["sim_01", "sim_02", "sim_03"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01", "sim_02", "sim_03"])
    ORDER.disablePath(name = "LM57-LM59")
    o1 = ORDER.gotoOrder(vehicle="sim_02",location="AP18")
    assert ORDER.isOrderFinished(uuid = o1, timeout=60)

def test_disablePath3():
    """禁用当前线路
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    init_pos(loc="AP15",name="sim_02")
    ORDER.terminateAll(vehicle = ["sim_01", "sim_02", "sim_03"])
    time.sleep(2)
    ORDER.dispatchable(name = ["sim_01", "sim_02", "sim_03"])
    o1 = ORDER.gotoOrder(vehicle="sim_02",location="AP16")
    time.sleep(1)
    ORDER.disablePath(name = "AP15-LM58")
    ORDER.disablePath(name = "LM58-LM54")
    time.sleep(2)
    detail = ORDER.orderDetails(orderId = o1)
    assert detail["state"] == "FAILED", "state = {}".format(detail["state"])

def test_getDisablePath():
    """查询当前禁用线路
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    time.sleep(1)
    ORDER.disablePath(name = "AP15-LM58")
    ORDER.disablePath(name = "LM58-LM54")
    time.sleep(2)
    d = ORDER.getDisablePaths()
    v = [{"id":'LM58-LM54'}, {"id":'AP15-LM58'}]
    print(d,v)
    assert d == v

def test_getDisablePoint():
    """查询当前禁用线路
    """
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    time.sleep(1)
    ORDER.disablePoint(name = "AP15")
    ORDER.disablePoint(name = "LM54")
    time.sleep(2)
    d = ORDER.getDisablePoints()
    v = [{"id":'LM54'}, {"id":'AP15'}]
    print(d, v)
    ORDER.enablePath(name="all")
    ORDER.enablePoint(name="all")
    assert d == v or d == [v[1], v[0]]

if __name__ == '__main__':
    pytest.main(["-v","--html=report.html", "--self-contained-html"])