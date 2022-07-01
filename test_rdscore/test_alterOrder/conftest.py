import sys
sys.path.append("..")
import pytest

from APILib.orderLib import *

# def send1000(c:OrderLib):
#     loc_list = ["AP29", "AP30", "AP31"]
#     for i in range(0,1000):
#         c.gotoOrder(location=random.choice(loc_list))



@pytest.fixture(scope="module")
def core():
    """执行这个脚本的用例前需要的准备内容
    """
    # start core
    c = OrderLib(getServerAddr())
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "rds_20220601233537.zip")
    c.uploadScene(p)
    c.modifyParam({"RDSDispatcher": {
        "ClearDBOnStart":True
    }})
    time.sleep(5)
    c.updateSimRobotState(
        {"vehicle_id":"sim_01",
        "speed":0.1}
    )
    c.updateSimRobotState(
        {"vehicle_id":"sim_02",
        "speed":0.1}
    )
    c.updateSimRobotState(
        {"vehicle_id":"sim_03",
        "speed":0.1}
    )

    # send1000()
    # finished_orders = 0
    # while finished_orders < 100:
    #     time.sleep(1)
    #     res = requests.get(c.ip+"/orders")
    #     # 解析，数出有多少个订单已经完成了

    return c
    # todo 等待一部分订单完成