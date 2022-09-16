import math
import sys
import time
import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib
import json

r = rbklib("192.168.9.14", push_flag=True)


def test_charger():
    """
    检测小车的充电功能
    """
    task = {
        "id": "CP35",
        "task_id": "247189465"
    }
    head, body = r.robot_task_gotarget_req(**task)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    st_time = time.time()
    while True:
        head, body = r.robot_status_task_req()
        body = json.loads(body)
        ed_time = time.time()
        if body["task_status"] == 2:
            # 执行任务中
            time.sleep(1)
        elif body["task_status"] == 4:
            time.sleep(1)
            break
        elif ed_time - st_time >= 60:
            # 任务超时
            assert False

    # 查询电池的状态是否为在充电
    head, body = r.robot_status_battery_req()
    body = json.loads(body)
    charging = body["charging"]
    assert charging, f"{body['err_msg']}"

if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])