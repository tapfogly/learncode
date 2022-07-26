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

def init_pos(loc:str, name:str, a:float = 0.0):
    ORDER.terminateAll(vehicle = name)
    ORDER.dispatchable(name = name)
    data = {
        "vehicle_id":name,
        "position_by_name": loc,
        "angle": a
    }
    ORDER.updateSimRobotState(json.dumps(data))
    ORDER.locked()
    time.sleep(1)

def test_1():
    """ 3393
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM120", name="AMB-02")
    init_pos(loc = "CP134", name="AMB-01")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP45")
    time.sleep(5)
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP68")


def test_2():
    """ 3393
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "AP73", name="AMB-02")
    init_pos(loc = "AP7", name="AMB-01", a = 1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP45")
    time.sleep(2.5)
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="PP50")

def test_3():
    """ 3389
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "AP46", name="AMB-02")
    init_pos(loc = "LM100", name="AMB-01")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    time.sleep(3)
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP132")


def test_4():
    """ 3390
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM100", name="AMB-02")
    init_pos(loc = "LM152", name="AMB-01")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP46")
    time.sleep(2)
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP139")

def test_5():
    """ 3387
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "AP73", name="AMB-02")
    init_pos(loc = "LM113", name="AMB-01")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    time.sleep(10)
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP41")

def test_6():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    init_pos(loc = "PP51", name="AMB-01", a = 1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="PP50")
    time.sleep(5.0)
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")

def test_7():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    init_pos(loc = "LM54", name="AMB-01", a = 0)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")
    time.sleep(5.0)
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="PP50")

def test_8():
    """ CP exchange, and return PP1
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    init_pos(loc = "LM154", name="AMB-01", a = 0)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")
    time.sleep(5.0)
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="PP50")

def test_9():
    """ CP exchange, and return PP2
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    init_pos(loc = "LM154", name="AMB-01", a = 0)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")
    time.sleep(5.0)
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="PP51")

def test_10():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM154", name="AMB-01")
    init_pos(loc = "LM160", name="AMB-02")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="LM160")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="LM154")

def test_11():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM169", name="AMB-01")
    init_pos(loc = "AP47", name="AMB-02")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP136")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP132")

def test_12():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "PP51", name="AMB-01")
    init_pos(loc = "CP134", name="AMB-02")
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP68")

def test_13():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM172", name="AMB-01")
    init_pos(loc = "AP47", name="AMB-02", a = 1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP132")

def test_14():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "PP50", name="AMB-01", a = 1.57)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP30")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP47")

def test_15():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "AP68", name="AMB-01", a = 1.57)
    init_pos(loc = "AP47", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP140")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP132")

def test_16():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "AP68", name="AMB-01", a = 1.57)
    init_pos(loc = "AP47", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP117")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP125")

def test_17():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM162", name="AMB-01", a = 1.57)
    init_pos(loc = "AP73", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP41")

def test_18():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM97", name="AMB-01", a = 1.57)
    init_pos(loc = "LM154", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP44")

def test_19():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM168", name="AMB-01", a = 1.57)
    init_pos(loc = "LM159", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP28")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP45")

def test_20():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM147", name="AMB-01", a = 1.57)
    init_pos(loc = "CP134", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="CP134")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="PP50")

def test_21():
    """ 
    """
    ORDER.terminateAll(vehicle = ["AMB-01", "AMB-02"])
    time.sleep(2)
    init_pos(loc = "LM169", name="AMB-01", a = -1.57)
    init_pos(loc = "LM138", name="AMB-02", a = -1.57)
    ORDER.dispatchable(name = ["AMB-01", "AMB-02"])
    o1 = ORDER.gotoOrder(vehicle="AMB-01",location="AP68")
    o2 = ORDER.gotoOrder(vehicle="AMB-02",location="AP45")

if __name__ == "__main__":
    # maybe fail: 
    # 3,13,19,20
    test_19()

