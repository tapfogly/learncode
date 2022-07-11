import sys
sys.path.append("../..")

from APILib.orderLib import *
import pytest

vehicle_name = "AMB-201"
def test_ignore_robot(core:OrderLib):
    """ 非dispatchable的车不能预接单
    """
    core.terminateAll(vehicle_name)
    time.sleep(5)
    core.dispatchable(vehicle_name)
    # 1. 发一个waiting单
    order_id = str(uuid.uuid1())
    order = {
        "id" : order_id,
        "blocks":[
            {
                "blockId":order_id+"_block",
                "location":"LM202"
            }
        ],
        "complete":False
    }
    requests.post(core.ip+'/setOrder', data=json.dumps(order))
    time.sleep(4)
    state = core.orderDetails(order_id)['state']
    
    while state not in ["RUNNING", "WAITING"]:
        time.sleep(2)
        state = core.orderDetails(order_id)['state']

    assert core.orderDetails(order_id)['vehicle'] == vehicle_name
    # 2. 设为undispatchable，再发单，不能预接单
    core.undispatchable_unignore(name=vehicle_name)
    time.sleep(2)
    order_id= core.gotoOrder(location="LM201")
    time.sleep(5)
    state = core.orderDetails(order_id)['state']
    while not state in ["TOBEDISPATCHED", "CREATED", "FINISHED", "STOPPED"]:
        time.sleep(2)
        state = core.orderDetails(order_id)['state']
    assert state == "TOBEDISPATCHED"

def test_re_dispatch():
    """ 车辆不可接单后，重新分配预接的单
    """
    

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])