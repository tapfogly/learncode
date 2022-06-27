import json
import time
import pytest


@pytest.fixture(scope='class', autouse=True)
def classFixture(rbk):
    # 测试开始时执行（初始化）
    # 让小车回到初始位置
    rbk.robot_task_gotarget_req(id="AP30")
    time.sleep(5)
    isComplete = False
    count = 0
    for i in range(40):
        body = json.loads(rbk.pushData.get())
        print(count, "当前站点:", body.get("current_station"), "任务状态:", body.get("task_status"))
        if body.get("task_status") == 4 and body.get("current_station") == "AP30":
            isComplete = True
            break
        count += 1
        time.sleep(1)
    if not isComplete or body.get("current_station") != "AP30":
        raise Exception("初始化失败")
    yield
    # 测试结束时执行（清理）
    rbk.robot_task_gotarget_req(id="AP32")
    isComplete = False
    count = 0
    for i in range(40):
        body = json.loads(rbk.pushData.get())
        print(count, "当前站点:", body.get("current_station"), "任务状态:", body.get("task_status"))
        if body.get("task_status") == 4 and body.get("current_station") == "AP32":
            isComplete = True
            break
        count += 1
        time.sleep(1)
    if not isComplete or body.get("current_station") != "AP32":
        raise Exception("清理失败")