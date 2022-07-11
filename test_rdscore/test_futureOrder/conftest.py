import sys
sys.path.append("../..")
from APILib.orderLib import *
import pytest


@pytest.fixture(scope="session")
def core():
    c = OrderLib(getServerAddr())
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "scene.zip")
    c.uploadScene(p)
    c.modifyParam({"RDSDispatcher":{"ClearDBOnStart":True, "ClearOldOrdersDisabled":True,"JoinableDist":99}})
    time.sleep(5)
    return c