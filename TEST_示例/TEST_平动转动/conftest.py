import json
import time

import pytest


@pytest.fixture()
def init(rbk):
    rbk.robot_task_gotarget_req(id="AP29")
    isComplete = False
    count = 0
    for i in range(40):
        body = json.loads(rbk.pushData.get())
        print(count, "当前站点:", body.get("current_station"), "任务状态:", body.get("task_status"))
        if body.get("task_status") == 4:
            isComplete = True
            break
        count += 1
        time.sleep(1)
    if not isComplete or body.get("current_station") != "AP29":
        raise Exception("初始化失败")