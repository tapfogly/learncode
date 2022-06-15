import json
import math
import time

import pytest


class Test_平动转动测试:
    @pytest.mark.translate
    @pytest.mark.usefixtures("init")
    @pytest.mark.parametrize("dist", [1, 2, 3, 4])
    def test_平动测试(self, rbk, dist):
        d = json.loads(rbk.pushData.get())
        ox = d.get("x")
        oy = d.get("y")
        print("x:", ox, "y:", oy)
        head, body = rbk.robot_task_translate_req(dist, 1, 1)
        body: dict = json.loads(body)
        assert body.get("ret_code") == 0
        isComplete = False
        for i in range(10):
            d = json.loads(rbk.pushData.get())
            print("x:", d.get("x"), "y:", d.get("y"), "task_status:", d.get("task_status"))
            if d.get("task_status") == 4:
                isComplete = True
                break
            time.sleep(1)
        if not isComplete:
            raise Exception("10秒内未完成任务")
        tx = d.get("x")
        ty = d.get("y")
        length = math.sqrt((tx - ox) ** 2 + (ty - oy) ** 2)
        print("length:", length)
        assert -0.1 < length - dist < 0.1

    @pytest.mark.turn
    @pytest.mark.parametrize("angle,vw",
                             [(30, 1), (60, 1), (90, 1), (120, 1), (150, 1), (180, 1), (210, 1), (240, 1), (270, 1),
                              (300, 1), (330, 1), (30, -1), (60, -1), (90, -1), (120, -1), (150, -1), (180, -1),
                              (210, -1), (240, -1), (270, -1), (300, -1), (330, -1)])
    def test_转动测试(self, rbk, angle, vw):
        body = json.loads(rbk.pushData.get())
        oAngle = body.get("angle")
        print("初始角度:", oAngle)
        rad = angle * math.pi / 180
        head, body = rbk.robot_task_turn_req(rad, vw)
        body: dict = json.loads(body)
        assert body.get("ret_code") == 0
        isComplete = False
        for i in range(10):
            body = json.loads(rbk.pushData.get())
            print("当前角度:", body.get("angle"), "任务状态:", body.get("task_status"))
            if body.get("task_status") == 4:
                isComplete = True
                break
            time.sleep(1)
        if not isComplete:
            raise Exception("10秒内未完成任务")
        tAngle = body.get("angle")
        print("结束角度:", tAngle)
        if angle < 0:
            assert tAngle == oAngle
        else:
            rAngle = math.fabs(tAngle - oAngle)
            if rAngle > math.pi:
                rAngle = 2 * math.pi - rAngle
            if rad > math.pi:
                rAngle = 2 * math.pi - rAngle
            print("差:", rAngle, "目标角度:", rad)
            assert -0.01 < rAngle - rad < 0.01
