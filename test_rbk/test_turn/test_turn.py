import sys
import math
import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib
import json
import time

r = rbklib("192.168.9.14", push_flag=True)


def turn(angle, vw):
    cmd = {
        "angle": angle,
        "vw": vw
    }
    old_rad = json.loads(r.pushData.get())["angle"]

    head, body = r.robot_task_turn_req(**cmd)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

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

    new_rad = json.loads(r.pushData.get())["angle"]

    rAngle = math.fabs(new_rad - old_rad)
    if rAngle > math.pi:
        rAngle = 2 * math.pi - rAngle
    if cmd["angle"] > math.pi:
        rAngle = 2 * math.pi - rAngle
    print("差:", rAngle, "目标角度:", cmd["angle"])
    assert -0.017 < rAngle - cmd["angle"] < 0.017


def test_turn():
    '''
    转动功能检查
    '''

    angle = 30
    rad = angle * math.pi / 180
    turn(rad, 0.3)
    turn(rad, -0.3)


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
