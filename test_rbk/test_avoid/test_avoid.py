import laserData1
import laserData3
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
def test_path():
    RBK.clearSimLaser()
    time.sleep(0.5)
    x = laserData1.x
    y = laserData1.y
    RBK.setSimLaser(x, y)
    pos = {"x":10.782701, "y":2.4977, "angle":-86.07}
    RBK.moveRobot(pos)
    data = {"id":"LM6"}
    RBK.sendTask(data)
    # plt.plot(x,y,'.')
    # plt.show()

def test_narrow_path():
    RBK.clearSimLaser()
    time.sleep(0.5)
    x = laserData3.x
    y = laserData3.y
    RBK.setSimLaser(x, y)
    pos = {"x":19.522, "y":4.0, "angle":179.734}
    RBK.moveRobot(pos)
    data = {"id":"AP17"}
    RBK.sendTask(data)
    # plt.plot(x,y,'.')
    # plt.show()

if __name__ == "__main__":
    test_path()
