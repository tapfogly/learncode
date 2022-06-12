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

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global core
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "rds_20220601233537.zip")
    core.uploadScene(p)
    time.sleep(5)

def test_without_label():
    '''
    发单时不一定需要下发label
    '''
    order_id = core.gotoOrder(location="AP23", group="g1")
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'

def test_good_label1():
    '''
    标签中有一辆车, 和group匹配
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "complete": True, "label":"two-group","group":"g1", "blocks": [
        {"blockId": str(uuid.uuid1()), "location": "AP24",
         "operation": "JackLoad",
         },
        {"blockId": str(uuid.uuid1()), "location": "AP25",
         "operation": "JackUnload",
         },
    ]}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'

def test_label_nonexistent():
    '''
    指定不存在的标签
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "complete": True, "label":"SSKSJLKSJSLKJ","group":"g1", "blocks": [
        {"blockId": str(uuid.uuid1()), "location": "AP26",
         "operation": "JackLoad",
         },
        {"blockId": str(uuid.uuid1()), "location": "AP27",
         "operation": "JackUnload",
         },
    ]}
    res = requests.post(f"{core.ip}/setOrder",
                        data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    print(detail)
    assert detail['state'] == 'STOPPED'
    assert detail['errors'][0]['code'] == 60014

def test_label_group_conflict():
    '''
    label 和 group 冲突
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "complete": True, "label":"one-robot","group":"g2", "blocks": [
        {"blockId": str(uuid.uuid1()), "location": "AP28",
         "operation": "JackLoad",
         },
        {"blockId": str(uuid.uuid1()), "location": "AP29",
         "operation": "JackUnload",
         },
    ]}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'STOPPED'
    assert detail['errors'][0]['code'] == 60013

def test_no_label_group():
    '''
    不指定label 和 group
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "complete": True, "blocks": [
        {"blockId": str(uuid.uuid1()), "location": "AP28",
         "operation": "JackLoad",
         },
        {"blockId": str(uuid.uuid1()), "location": "AP29",
         "operation": "JackUnload",
         },
    ]}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'

# simple order


def test_without_label_simple_order():
    '''
    发拼单任务时没有标签
    '''
    order_id = str(uuid.uuid1())
    simple_order = {"id": order_id, "fromLoc": "WS-1-8",
                    "toLoc": "WS-1-9", "group": "g1", "goodsId": "test"}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(simple_order))

    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'


def test_good_label_simple_order1():
    '''
    标签中有一辆车, 和group匹配
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "label": "two-group", "group": "g1",
             "fromLoc": "WS-1-8", "toLoc": "WS-1-10", "goodsId": "test"}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'

def test_label_nonexistent_simple_order():
    '''
    指定不存在的标签
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id,  "label":"SSKSJLKSJSLKJ","group":"g1", "fromLoc": "WS-1-8", "toLoc": "WS-1-10", "goodsId": "test"}
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    print(detail)
    assert detail['state'] == 'STOPPED'
    assert detail['errors'][0]['code'] == 60014

def test_label_group_conflict_simple_order():
    '''
    label 和 group 冲突
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "label":"one-robot","group":"g2", "fromLoc": "WS-1-8", "toLoc": "WS-1-10"   }
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'STOPPED'
    assert detail['errors'][0]['code'] == 60013

def test_no_label_and_group_conflict_simple_order():
    '''
    不指定label 和 group
    '''
    order_id = str(uuid.uuid1())
    order = {"id": order_id, "fromLoc": "WS-1-8", "toLoc": "WS-1-10"   }
    requests.post(f"{core.ip}/setOrder", data=json.dumps(order))
    core.waitForOrderFinish(order_id)
    detail = core.orderDetails(order_id)
    assert detail['state'] == 'FINISHED'

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
