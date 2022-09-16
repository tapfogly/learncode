import sys
import math
import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib
import json
import time

r = rbklib("192.168.9.14", push_flag=True)


def test_target():
    """
    下发任务，暂停任务，继续执行任务
    """
    target = "AP27"
    cmd = {
        "id": target,
        "task_id": "12356375"
    }

    # 执行任务
    head, body = r.robot_task_gotarget_req(**cmd)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    # 任务暂停
    head, body = r.robot_task_pause_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    # 判断任务是否暂停
    head, body = r.robot_status_task_req()
    body = json.loads(body)
    assert body["task_status"] == 3

    time.sleep(2)

    # 恢复任务
    head, body = r.robot_task_resume_req()
    body = json.loads(body)
    assert body["ret_code"] == 0

    start = time.time()
    while True:
        end = time.time()
        body = json.loads(r.pushData.get())
        if end - start >= 20:
            break
        elif body["task_status"] == 2:
            time.sleep(1)
            continue
        elif body["task_status"] == 4:
            break

    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["current_station"] == target


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
