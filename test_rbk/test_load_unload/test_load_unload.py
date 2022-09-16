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
    检测顶升车取货放货功能
    """
    # 取货动作
    target = "AP22"
    task = {
        "id": target,
        "task_id": "247189465",
        "operation": "JackLoad",
        "jack_height": 0.03,
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
        elif ed_time - st_time >= 30:
            # 任务超时
            assert False

    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["current_station"] == target

    # 放货动作
    target = "AP25"
    task = {
        "id": target,
        "task_id": "658489465",
        "operation": "JackUnload",
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
        elif ed_time - st_time >= 30:
            # 任务超时
            assert False

    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["current_station"] == target


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
