import json
import time
import pytest


@pytest.fixture(scope='class', autouse=True)
def classFixture(rbk):
    # 测试开始时执行（初始化）
    # 让小车回到初始位置
    rbk.robot_task_gotarget_req(id="AP30")
    result = False
    for i in range(40):
        body = json.loads(rbk.pushData.get())
        if body.get("current_station") == "AP30":
            result = True
            break
        time.sleep(1)
    if not result:
        pytest.exit("初始化失败，请检查")
    yield
    # 测试结束时执行（清理）
    rbk.robot_task_gotarget_req(id="AP32")
    result = False
    for i in range(40):
        body = json.loads(rbk.pushData.get())
        if body.get("current_station") == "AP32":
            result = True
            break
        time.sleep(1)
    if not result:
        pytest.exit("清理失败")