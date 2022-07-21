import sys
from pathlib import Path
import numpy as np

sys.path.append(Path(__file__).parents[2])
from APILib.orderLib import *

core = OrderLib(getServerAddr())


def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    # core.modifyParam({"RDSDispatcher":{"AutoPark":False}})
    # core.uploadScene(Path(Path(__file__).absolute().parent,"lvyuan.zip"))
    # time.sleep(60) # 更新很慢


def set_sim_pos_by_name(vehicle, pos_name):
    core.updateSimRobotState(json.dumps({"vehicle_id": vehicle, "position_by_name": pos_name}))


def set_sim_goods_shape(vehicle, goods_shape):
    core.updateSimRobotState(json.dumps({"vehicle_id": vehicle, "goods_shape": goods_shape}))


def set_sim_goods_vehicle_angle(vehicle, goods_vehicle_angle):
    core.updateSimRobotState(json.dumps({"vehicle_id": vehicle, "goods_vehicle_angle": goods_vehicle_angle}))


v1, p1, pos1, target1 = "jack-54", "LM456", [-37.778, 49.444], "LM458"
v2, p2, pos2, target2 = "jack-70", "LM459", [-48.185, 51.734], "LM457"

large_goods_box = [-0.5, -1.5, 0.5, 1.5]


def test_goods_collision():
    """车不动，旋转货物
    """
    core.terminateAll([])
    time.sleep(3)
    core.dispatchable(v1)
    core.dispatchable(v2)
    time.sleep(3)

    set_sim_pos_by_name(v1, p1)
    set_sim_pos_by_name(v2, p2)
    # 设置货物
    set_sim_goods_shape(v1, large_goods_box)
    set_sim_goods_shape(v2, large_goods_box)
    time.sleep(1)

    # set_sim_goods_vehicle_angle(v2, -1.57)

    order_id1 = core.gotoOrder(vehicle=v1, location=target1)
    order_id2 = core.gotoOrder(vehicle=v2, location=target2)

    core.waitForOrderFinish(order_id1)
    core.waitForOrderFinish(order_id2)


def test_goods_collision2():
    """车不动，旋转货物
    """
    core.terminateAll([])
    time.sleep(3)
    core.dispatchable(v1)
    core.dispatchable(v2)
    time.sleep(3)

    set_sim_pos_by_name(v1, p1)
    set_sim_pos_by_name(v2, p2)
    # 设置货物
    set_sim_goods_shape(v1, large_goods_box)
    set_sim_goods_shape(v2, large_goods_box)
    time.sleep(1)

    set_sim_goods_vehicle_angle(v2, 0)
    time.sleep(2)

    order_id1 = core.gotoOrder(vehicle=v1, location=target1)
    order_id2 = core.gotoOrder(vehicle=v2, location=target2)

    core.waitForOrderFinish(order_id1)
    core.waitForOrderFinish(order_id2)


def test_goods_collision3():
    """车不动，旋转货物
    """
    core.terminateAll([])
    time.sleep(3)
    core.dispatchable(v1)
    core.dispatchable(v2)
    time.sleep(3)

    set_sim_pos_by_name(v1, p1)
    set_sim_pos_by_name(v2, p2)
    # 设置货物
    set_sim_goods_shape(v1, large_goods_box)
    set_sim_goods_shape(v2, large_goods_box)
    time.sleep(1)

    set_sim_goods_vehicle_angle(v2, -1.57)
    set_sim_goods_vehicle_angle(v1, -1.57)
    time.sleep(2)

    order_id1 = core.gotoOrder(vehicle=v1, location=target1)
    order_id2 = core.gotoOrder(vehicle=v2, location=target2)

    core.waitForOrderFinish(order_id1)
    core.waitForOrderFinish(order_id2)
