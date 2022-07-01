'''robokit#1122 修改订单的label和priority字段'''

import sys
sys.path.append("../..")
import pytest

from APILib.orderLib import *



def test_alter_label_of_to_be_dispatched_order(core:OrderLib):
    '''
    修改未分配订单的label
    修改后，确认订单正确分配
    '''

    order_id = str(uuid.uuid1())
    order = {"id":order_id, "complete":False}
    requests.post(core.ip+"/setOrder", data= json.dumps(order))
    time.sleep(5)
    detail = core.orderDetails(order_id)
    assert detail["state"] == "TOBEDISPATCHED"

    core.setOrderLabel(order_id, "one-robot")
    time.sleep(5)
    detail = core.orderDetails(order_id)
    assert detail['label'] == "one-robot"
    ## todo 
    # print(detail)
    # assert detail["vehicle"] == "sim_03"
    # core.markComplete(order_id)


def test_alter_label_of_running_order(core:OrderLib):
    '''
    修改正在执行的订单的label
    '''
    order_id = core.gotoOrder(location="PS-1-5",label="one-robot")
    time.sleep(5)
    detail = core.orderDetails(order_id)
    assert detail['state'] == "RUNNING"
    core.setOrderLabel(order_id, "two-group")
    time.sleep(2)
    detail = core.orderDetails(order_id)
    assert detail['label'] == 'one-robot'


def test_alter_priority_of_to_be_dispatched_order(core:OrderLib):
    '''
    修改未分配订单的优先级
    修改后，确认订单正确分配
    '''
    order_id = str(uuid.uuid1())
    order = {
        "id":order_id,
        "priority":12,
        "complete":False
    }
    requests.post(core.ip+'/setOrder', data=json.dumps(order))
    time.sleep(5)
    detail = core.orderDetails(order_id)
    assert detail['state'] == "TOBEDISPATCHED"
    core.setOrderPriority(order_id, 1234)
    time.sleep(3)
    detail = core.orderDetails(order_id)
    assert detail['priority'] == 1234

def test_alter_priority_of_running_order(core:OrderLib):
    '''
    修改正在执行的订单的priority
    '''
    order_id = core.gotoOrder(location="WS-1-5", priority=12)
    time.sleep(5)
    detail = core.orderDetails(order_id)
    assert detail['state'] == "RUNNING"
    core.setOrderPriority(order_id, 12345)
    time.sleep(3)
    detail = core.orderDetails(order_id)
    assert detail['priority'] == 12

if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])