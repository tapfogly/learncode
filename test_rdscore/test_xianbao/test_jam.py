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

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "v0.zip")
    ORDER.uploadScene(p)
    time.sleep(5)
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "G-MAPF":True,
        "G-MAPF-Leaves":True,
        "G-MAPF-MovablePark": True,
        "G-MAPF-Physical":True
        }})

def teardown_module():
    # ORDER.terminateIdList([])
    pass

    
def test_jam():
    '''
    查看是否能够解死锁
    '''
    osim02 = ORDER.gotoOrder(location="D06-01-04-1", goodsId="C1-00025", vehicle="sim_02",group="BOX")
    osim09 = ORDER.gotoOrder(location="D06-01-03-2", goodsId="C1-00018", vehicle="sim_09",group="BOX")
    osim11 = ORDER.gotoOrder(location="D05-2-03-1", goodsId="C1-00013", vehicle="sim_11",group="BOX")
    osim12 = ORDER.gotoOrder(location="D05-4-09-1", goodsId="C1-00039", vehicle="sim_12",group="BOX")
    osim08 = ORDER.gotoOrder(location="D06-01-06-1", goodsId="C1-00041", vehicle="sim_08",group="BOX")
    osim10 = ORDER.gotoOrder(location="D06-01-07-2", goodsId="C1-00050",vehicle="sim_10",group="BOX")
    while True:
        time.sleep(1.0)
        o1 = ORDER.orderDetails(orderId = osim02)
        o2 = ORDER.orderDetails(orderId = osim09)
        o3 = ORDER.orderDetails(orderId = osim11)
        o4 = ORDER.orderDetails(orderId = osim12)
        o5 = ORDER.orderDetails(orderId = osim08)
        o6 = ORDER.orderDetails(orderId = osim10)
        if o1["state"] == "FINISHED" \
            and o2["state"] == "FINISHED"\
                and o3["state"] == "FINISHED"\
                    and o4["state"] == "FINISHED"\
                        and o5["state"] == "FINISHED"\
                            and o6["state"] == "FINISHED":
            assert True
            break
        rs = ORDER.robotsStatus()
        for e in rs["alarms"]["errors"]:
            if e["code"] != 52103 and e["code"] != 52101:
                assert False, "failed. has error {}".format(e)

if __name__ == "__main__":
    pytest.main(["-k test_jam", "-v", "--html=report.html", "--self-contained-html"])