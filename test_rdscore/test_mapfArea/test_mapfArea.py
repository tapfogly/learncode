# order_issue_pool#443 的测试用例
import json
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.orderLib import *
import time
from multiprocessing import freeze_support
import pytest

ORDER = OrderLib(getServerAddr())

class PostData:
    def __init__(self):
        print("发送任务")

    def setoder(self,fromloc,toloc,dv,addr="http://127.0.0.1:8088/setOrder"):
        self.addr = addr
        self.dv=dv
        self.fromLoc = fromloc
        self.toLoc = toloc
        self.head = {'Content-Type': 'application/json'}
        self.id = str(time.time()) + "man" + self.fromLoc
        self.data = json.dumps(
            {
                "fromLoc": self.fromLoc,
                "toLoc": self.toLoc,
                "id": self.id,
                "vehicle": self.dv
            }
        )
        res = requests.post(self.addr, data=self.data, headers=self.head)
        print(res,self.data)
        return self.id

post=PostData()

def init_pos():
    ORDER.terminateAll(vehicle = ["BR-01","BR-02","BR-03","Line-04"])
    ORDER.dispatchable(name = "BR-01")
    ORDER.dispatchable(name = "BR-02")
    ORDER.dispatchable(name = "BR-03")
    ORDER.dispatchable(name = "Line-04")
    ORDER.updateSimRobotState(json.dumps({"vehicle_id":"BR-01","position_by_name":"PP9037"}))
    ORDER.updateSimRobotState(json.dumps({"vehicle_id":"BR-02","position_by_name":"PP9039"}))
    ORDER.updateSimRobotState(json.dumps({"vehicle_id":"BR-03","position_by_name":"PP9130"}))
    ORDER.updateSimRobotState(json.dumps({"vehicle_id":"Line-04","position_by_name":"CP430"}))
    ORDER.locked()

def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global ORDER
    ORDER.uploadScene("test_rdscore/test_mapfArea/scene.zip")
    print("setup_module ...")
    time.sleep(5)

def test_1():
    """ 测试能否正常运行
    """
    ORDER.recoveryParam()
    ORDER.modifyParam({"RDSDispatcher":{
        "ClearDBOnStart":True,
        "G-MAPF":True,
        "G-MAPF-Physical":True,
        "G-MAPF-Vision":80,
        }})
    init_pos()
    post=PostData()
    id1 = post.setoder("AP4001","AP4002","BR-03")
    id2 = post.setoder("AP4003","AP4004","BR-01")
    id3 = post.setoder("AP4005","AP4006","BR-02")
    id4 = post.setoder("AP424","AP442","Line-04")
    start_t = time.time()
    num_finished = 0
    while True:
        time.sleep(2.0)
        dt = time.time() - start_t
        if num_finished == 0:
            oid = id1
        elif num_finished == 1:
            oid = id2
        elif num_finished == 2:
            oid = id3
        elif num_finished == 3:
            oid = id4
        else:
            assert True
            break
        O = ORDER.orderDetails(orderId=oid)
        if dt > 300:
            ORDER.terminateId(order_id=oid)
            assert False, "time out 300s. order status is {}".format(O["state"])
        if "state" not in O:
            continue
        if O["state"] == "RUNNING" or O["state"] == "CREATED" or O["state"] == "TOBEDISPATCHED":
            continue
        elif O["state"]  == "FINISHED":
            num_finished = num_finished + 1
            assert True
        else:
            assert False, "cannot work. order status is {}".format(O["state"])
def test_3():
    """ 指定机器人去一个不存在的点
    """
    o1 = ORDER.gotoOrder(vehicle="BR-03", location="LM419")
    time.sleep(1)
    d = ORDER.orderDetails(orderId = o1)
    assert d["state"] == "STOPPED"

if __name__ == "__main__":
    test_1()










