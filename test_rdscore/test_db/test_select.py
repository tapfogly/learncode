import pytest
import sys
sys.path.append("../..")
from APILib.orderLib import *


@pytest.mark.skip(reason="dev")
def test_select_order(core: OrderLib, db_select):
    j = core.pagedQuery(path="orders", relation="AND", predicates=[
        ["state", "EQ", "FINISHED"]])
    for order in j['list']:
        assert order['state'] == "FINISHED"


@pytest.mark.skip(reason="dev")
def test_select_block(core: OrderLib, db_select):
    j = core.pagedQuery(path="blocks", relation="AND", predicates=[["state", "EQ", "FINISHED"]])
    for block in j['list']:
        assert block['state'] == "FINISHED"


def test_select_max_page_size(core: OrderLib, db_select):
    '''测试分页查询的最大单页数据条数
    '''
    # 1 上传场景? 不需要上传场景
    # 2 发很多失败的订单
    order_num = 123456
    false_target = "锦绣申江11号楼3层306会议室"
    s = requests.Session()
    for i in range(1, order_num):
        s.post(core.ip+"/setOrder", data=json.dumps(
            {
                "id":str(uuid.uuid1()),
                "keyRoute": [false_target],
                "complete":True
            }
        ),headers={'Content-Type': 'application/json', 'Connection':'Keep-Alive'})
    # 3 查询
    j = core.pagedQuery(path="orders", page_size=order_num)
    print(j['size'])
    with open('data.json', 'w') as f:
        json.dump(j, f, indent=4)
    assert(j['size'] == order_num)



if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])


