import pytest
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.orderLib import *

core = OrderLib(getServerAddr())

# def setup_module():
#     """执行这个脚本的用例前需要的准备内容
#     """
#     global core
#     p = os.path.abspath(__file__)
#     p = os.path.dirname(p)
#     p = os.path.join(p, "japan_scene.zip")
#     core.uploadScene(p)
#     time.sleep(5)

def init_pos(loc:str, name:str, a:float):
    core.terminateAll(vehicle = name)
    core.dispatchable(name = name)
    data = {
        "vehicle_id":name,
        "position_by_name": loc,
        "angle": a
    }
    core.updateSimRobotState(json.dumps(data))
    core.locked()
    time.sleep(1)

def test_1():
    '''
    测试机器人设置为，占用资源，但是等待当前运单执行完成，看起是否运单完成后接单
    '''
    core.terminateAll(vehicle = ["AMB-200"])
    time.sleep(2)
    init_pos(loc = "AP92", name="AMB-200",a=1.57)
    core.dispatchable(name = ["AMB-200"])
    o1 = core.gotoOrder(vehicle="AMB-200",location="AP97")
    time.sleep(1)
    core.undispatchable_unignore("AMB-200", True)
    core.waitForOrderFinish(o1)
    o2 = core.gotoOrder(vehicle="AMB-200",location="LM255")
    time.sleep(1)
    detail = core.orderDetails(o2)
    core.terminateId(o2)
    core.terminateId(o1)
    assert detail['state'] == "TOBEDISPATCHED"

def test_2():
    '''
    测试机器人设置为，占用资源，看看机器人是否停在那里
    '''
    core.terminateAll(vehicle = ["AMB-200"])
    time.sleep(2)
    init_pos(loc = "AP92", name="AMB-200",a=1.57)
    core.dispatchable(name = ["AMB-200"])
    o1 = core.gotoOrder(vehicle="AMB-200",location="LM380")
    time.sleep(1)
    core.undispatchable_unignore("AMB-200")
    time.sleep(1)
    detail = core.orderDetails(o1)
    core.terminateId(o1)
    assert detail['state'] == "RUNNING"


def test_3():
    '''
    测试机器人设置为，不占用资源，但是等待当前运单执行完成，看起是否运单完成后接单
    '''
    core.terminateAll(vehicle = ["AMB-200"])
    time.sleep(2)
    init_pos(loc = "AP92", name="AMB-200",a=1.57)
    core.dispatchable(name = ["AMB-200"])
    o1 = core.gotoOrder(vehicle="AMB-200",location="AP97")
    time.sleep(1)
    core.undispatchable_ignore("AMB-200", True)
    core.waitForOrderFinish(o1)
    o2 = core.gotoOrder(vehicle="AMB-200",location="LM255")
    time.sleep(1)
    detail = core.orderDetails(o2)
    core.terminateId(o2)
    core.terminateId(o1)
    assert detail['state'] == "TOBEDISPATCHED"

def test_4():
    '''
    测试机器人设置为，不占用资源，看看机器人是否停在那里
    '''
    core.terminateAll(vehicle = ["AMB-200"])
    time.sleep(2)
    init_pos(loc = "AP92", name="AMB-200",a=1.57)
    core.dispatchable(name = ["AMB-200"])
    o1 = core.gotoOrder(vehicle="AMB-200",location="LM380")
    time.sleep(1)
    core.undispatchable_ignore("AMB-200")
    time.sleep(1)
    detail = core.orderDetails(o1)
    core.terminateId(o1)
    assert detail['state'] == "RUNNING"

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
