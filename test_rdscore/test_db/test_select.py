import pytest
import sys
sys.path.append("../..")
from APILib.orderLib import *


def test_select_order(core: OrderLib, db_select):
    j = core.pagedQuery(path="orders", relation="AND", predicates=[
        ["state", "EQ", "FINISHED"]])
    for order in j['list']:
        assert order['state'] == "FINISHED"


def test_select_block(core: OrderLib, db_select):
    j = core.pagedQuery(path="blocks", relation="AND", predicates=[["state", "EQ", "FINISHED"]])
    for block in j['list']:
        assert block['state'] == "FINISHED"



if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
