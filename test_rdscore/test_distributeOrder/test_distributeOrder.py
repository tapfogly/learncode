import sys
from pathlib import Path

sys.path.append(Path(__file__).absolute().parents[2])
from APILib.orderLib import *

core = OrderLib(getServerAddr())


def module_setup():
    pass


def test_send_distribute_order():
    """
    下发分拨单
    """
    s = requests.session()
    order_id = str(uuid.uuid1())
    distribute_order = {
        "id": order_id,
        "externalId": "xxx",
        "fromLoc": "AP16",
        "ordered": True,
        "toLocList": ["AP27", "AP28", "WS-1-5"]
    }
    res = s.post(core.ip + '/setOrder', data=json.dumps(distribute_order))
    # todo 查询状态
    time.sleep(2)

    details = core.pagedQuery("distributeOrders")
    print(details)

def test_execute_distribute_order():
    """
    执行分拨单
    """
    s = requests.session()
    order_id = str(uuid.uuid1())
    distribute_order = {
        "id":order_id,
        "externalId":"xxx",
        "fromLoc":"AP16",
        "ordered":True,
        "toLocList":["AP27","AP28","WS-1-5"]
    }
    res = s.post(core.ip+'/setOrder',data=json.dumps(distribute_order))
    time.sleep(2)

    detail = s.get(f'{core.ip}/distributeOrderDetails/{order_id}')
