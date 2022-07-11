import sys
sys.path.append("../..")

from APILib.orderLib import *

import pytest

vehicle_id = "AMB-201"

def test_odo(core:OrderLib):
    order_id = core.gotoOrder(location="LM173")
    core.waitForOrderFinish(order_id)
    details = core.orderDetails(order_id)
    assert details['state'] == "FINISHED"
    assert details['finishOdo'] > details['startOdo']

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])