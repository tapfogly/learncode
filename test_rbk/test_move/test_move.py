import sys

import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib
import json
import time

r = rbklib("192.168.9.14", push_flag=True)


def test_robot_translate():
    '''
    平动功能检查
    '''
    d = {
        "dist": 5,
        "vx": 1
    }

    head, body = r.robot_task_translate_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    odo = json.loads(r.pushData.get())["odo"]
    start = time.time()
    while True:
        end = time.time()
        body = json.loads(r.pushData.get())
        if end - start >= 30:
            break
        elif body["task_status"] == 2:
            time.sleep(1)
            continue
        elif body["task_status"] == 4:
            break

    end_odo = json.loads(r.pushData.get())["odo"]
    assert 5.1 >= end_odo - odo >= 4.9, "行走里程数不匹配"


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
