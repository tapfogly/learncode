# import pytest
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.rbklib import *
import matplotlib.pyplot as plt

RBK = rbklib(getIP())

def test_unload_error():
    RBK.recoveryParam()
    RBK.modifyParam(data = {"MoveFactory":{"CollisionPointNum":5}})
    RBK.modifyParam(data = {"RBKSim":{"RBKSimLaserMinDist":0.3}})
    RBK.clearSimLaser()
    RBK.setSimLaser([9], [8])
    pos = {"x":13.743, "y":7.961, "angle":-180}
    RBK.moveRobot(pos)
    task_cmd = {
        "id": "LM1"
    }
    RBK.sendTask(task_cmd)

if __name__ == "__main__":
    test_unload_error()