import sys
import math
import pytest

sys.path.append("..")
from APILib.rbklib import rbklib
from APILib.common import *


def setup_module():
    open_ip = None
    model = None
    s_id = None
    task_id = None
    charger_name = None
    with open("config.json", "r") as f:
        body = json.loads(f.read())
        open_ip = body["ip"]
        model = body["model_name"]
        s_id = body["source_id"]
        task_id = body["id"]
        charger_name = body["charger_name"]
    return open_ip, model, s_id, task_id, charger_name


ip, model_name, source_id, task, charger = setup_module()
r = rbklib(ip, push_flag=True)
r.robot_config_lock_req("test_robot")
current_map: str = ""

"""============================================================================
================================= 机器人状态API =================================
============================================================================"""


def test_rbk_info():
    rbk_info(r)


def test_rbk_run():
    rbk_run(r)


def test_rbk_loc():
    rbk_loc(r)


def test_rbk_speed():
    rbk_speed(r)


def test_rbk_block():
    rbk_block(r)


def test_rbk_battery():
    rbk_battery(r)


def test_rbk_motor():
    rbk_motor(r)


def test_rbk_laser():
    rbk_laser(r)


def test_rbk_area():
    rbk_area(r)


def test_rbk_emergency():
    rbk_emergency(r)


def test_rbk_io():
    rbk_io(r)


def test_rbk_imu():
    rbk_imu(r)


def test_rbk_rfid():
    rbk_rfid(r)


def test_rbk_ultrasonic():
    rbk_ultrasonic(r)


def test_rbk_pgv():
    rbk_pgv(r)


def test_rbk_encoder():
    rbk_encoder(r)


def test_rbk_task():
    rbk_task(r)


def test_rbk_task_package():
    rbk_task_package(r)


def test_rbk_reloc():
    rbk_reloc(r)


def test_rbk_loadmap():
    rbk_loadmap(r)


def test_rbk_slam():
    rbk_slam(r)


def test_rbk_jack():
    rbk_jack(r)


def test_rbk_fork():
    rbk_fork(r)


def test_rbk_roller():
    rbk_roller(r)


def test_rbk_dispatch():
    rbk_dispatch(r)


def test_rbk_alarm():
    rbk_alarm(r)


def test_rbk_all1():
    rbk_all1(r)


def test_rbk_all2():
    rbk_all2(r)


def test_rbk_all3():
    rbk_all3(r)


def test_rbk_current_lock():
    rbk_current_lock(r)


def test_rbk_map():
    rbk_map(r)


def test_rbk_station():
    rbk_station(r)


def test_rbk_mapmd5():
    rbk_mapmd5(r)


def test_rbk_params():
    rbk_params(r)


def test_rbk_model():
    rbk_model(r, model_name)


def test_rbk_downloadfile():
    rbk_downloadfile(r)


def test_rbk_canframe():
    rbk_canframe(r)


def test_rbk_transparent():
    rbk_transparent(r)


def test_rbk_gnsscheck():
    rbk_gnsscheck(r)


def test_rbk_gnss_list():
    rbk_gnss_list(r)


def test_rbk_sound():
    rbk_sound(r)


"""============================================================================
================================= 机器人控制API =================================
============================================================================"""


def test_reloc():
    reloc(r)


def test_clear_motor():
    clear_motor(r)


def test_loadmap():
    loadmap(r)


def test_uploadmap():
    uploadmap(r)


"""============================================================================
================================= 机器人配置API =================================
============================================================================"""


def test_upload():
    upload(r)


def test_src():
    src(r)


def test_src_release():
    src(r)


def test_set_clear_error():
    set_clear_error(r)


def test_set_clear_warning():
    set_clear_warning(r)


def test_setparams():
    setparams(r)


def test_saveparams():
    saveparams(r)


def test_obstacle():
    obstacle(r)


def test_clear_all_err():
    clear_all_err(r)


def test_motor():
    motor(r)


"""============================================================================
================================= 机器人其它API =================================
============================================================================"""


def test_peripheral_data():
    peripheral_data(r)


def test_update_transparent():
    update_transparent(r)


def test_softemc():
    softemc(r)


def test_audio():
    audio(r)


"""============================================================================
================================= 机器人导航API =================================
============================================================================"""


def test_precision():
    """
    运动到点精度
    """
    time.sleep(2)
    r = rbklib(ip, push_flag=True)
    r.lock()

    d = {
        "source_id": source_id,
        "id": task,
        "task_id": "test_amb300"
    }

    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    """
    查看机器人导航状态
    """
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
    time.sleep(2)
    """
    获取机器人当前的位置信息
    """
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x1, y1 = body["x"], body["y"]
    print("x1 = ", x1, " y1", y1)
    """
    查询目标点信息
    """
    head, body = r.robot_status_station()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x2, y2 = None, None
    for i in range(len(body["stations"])):
        if body["stations"][i]["id"] == task:
            x2 = body["stations"][i]["x"]
            y2 = body["stations"][i]["y"]
    print("x2 = ", x2, "y2 = ", y2)
    assert 0.02 >= abs(x2 - x1) and 0.02 >= abs(y2 - y1)
    time.sleep(2)


def test_robot_turn():
    """
    转动
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ck7o3v
    """
    angle = 180
    rad = angle * math.pi / 180
    d = {
        "angle": rad,
        "vw": 0.3
    }

    old_rad = json.loads(r.pushData.get())["angle"]

    head, body = r.robot_task_turn_req(**d)
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

    time.sleep(2)

    new_rad = json.loads(r.pushData.get())["angle"]

    rAngle = math.fabs(new_rad - old_rad)
    if rAngle > math.pi:
        rAngle = 2 * math.pi - rAngle
    if rad > math.pi:
        rAngle = 2 * math.pi - rAngle
    print("差:", rAngle, "目标角度:", rad)
    assert -0.017 < rAngle - rad < 0.017


def test_robot_translate():
    """
    平动
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lz24sz
    """
    time.sleep(2)

    d = {
        "dist": 1,
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
        if end - start >= 1000:
            break
        elif body["task_status"] == 2:
            time.sleep(1)
            continue
        elif body["task_status"] == 4:
            break

    end_odo = json.loads(r.pushData.get())["odo"]
    assert 1.03 >= end_odo - odo >= 0.07, "行走里程数不匹配"


"""============================================================================
================================= 其他测试 =====================================
============================================================================"""


def test_charge_start_time():
    """
    测试小车充电模型文件配置
    """

    head, body = r.robot_status_model_req()
    body = json.loads(body)
    device_type = body["deviceTypes"]

    ok = True
    for i in range(len(device_type)):
        if device_type[i]["name"] == "charger":
            param = device_type[i]["devices"]
            for k in range(len(param)):
                if param[k]["name"] == "charger":
                    device_param = param[k]["deviceParams"]
                    for j in range(len(device_param)):
                        if device_param[j]["key"] == "basic":
                            com = device_param[j]["arrayParam"]["params"]
                            for z in range(len(com)):
                                if com[z]["key"] == "chargeStartTime":
                                    charger_time = com[z]["doubleValue"]
                                    if charger_time <= 0:
                                        print("chargeStartTime < 0")
                                        assert False
                                        # com[z]["doubleValue"] = 20
                                        # ok = False

    if ok:
        assert True
    else:
        with open("robot.model", "w") as f:
            f.write(json.dumps(body, separators=(",", ":")))

            # 修改好的模型文件
            path = "robot.model"
            head, body = r.robot_config_model_req(path)
            body = json.loads(body)
            assert body["ret_code"] == 0


#
# def test_battery():
#     """
#     充电检查
#     """
#     # 去充电桩
#     d = {
#         "id": charger
#     }
#     head, body = r.robot_task_gotarget_req(**d)
#     body = json.loads(body)
#     assert body["ret_code"] == 0
#
#     start = time.time()
#     while True:
#         end = time.time()
#         body = json.loads(r.pushData.get())
#         if body["task_status"] == 2:
#             time.sleep(1)
#         elif body["task_status"] == 4:
#             break
#
#     # 离开充电桩
#     d = {
#         "id": source_id
#     }
#     head, body = r.robot_task_gotarget_req(**d)
#     body = json.loads(body)
#     assert body["ret_code"] == 0
#
#     start = time.time()
#     while True:
#         end = time.time()
#         body = json.loads(r.pushData.get())
#         if end - start >= 30:
#             break
#         elif body["task_status"] == 2:
#             time.sleep(1)
#         elif body["task_status"] == 4:
#             break
#
#     time.sleep(1)
#
#     # 查询充电状态
#     head, body = r.robot_status_battery_req()
#     body = json.loads(body)
#     assert body["ret_code"] == 0
#
#     # 如果离开充电桩仍充电那么存在问题
#     if not body["charging"]:
#         assert True
#     else:
#         assert False


def test_opera():
    """
    带动作的导航任务  料箱车取货
    """
    d = {
        "id": "SELF_POSITION",
        "source_id": "SELF_POSITION",
        "task_id": "12345678abcdefgh",
        "operation": "Script",
        "script_args": {
            "lift": 1350,
            "operation": "load",
            "recAdjust": 1,
            "rotate": -1.57,
            "stretch": 900,
            "visionType": "box"
        },
        "script_name": "ctuNoBlock.py"
    }
    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0

    """
    查看机器人导航状态
    """
    st_time = time.time()
    while True:
        body = json.loads(r.pushData.get())
        ed_time = time.time()
        assert body["ret_code"] == 0
        if body["task_status"] == 2:
            # 执行任务中
            time.sleep(1)
        elif body["task_status"] == 4:
            break
        elif ed_time - st_time >= 20:
            # 任务超时
            assert False

    """
    带动作的导航任务  料箱车卸货
    """
    d = {
        "id": "SELF_POSITION",
        "source_id": "SELF_POSITION",
        "task_id": "12345678abcdefgh",
        "operation": "Script",
        "script_args": {
            "lift": 1350,
            "operation": "unload",
            "recAdjust": 1,
            "rotate": -1.57,
            "stretch": 900,
            "visionType": "shelf"
        },
        "script_name": "ctuNoBlock.py"
    }
    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0


def test_move_check():
    """
    料箱车模型文件检查
    """
    r = rbklib(ip)
    r.lock()
    head, body = r.robot_status_model_req()
    body = json.loads(body)
    device_type = body["deviceTypes"]

    script_name = ""
    script_args = ""
    for i in range(len(device_type)):
        if device_type[i]["name"] == "safeMoveCheck":
            param = device_type[i]["devices"]
            for k in range(len(param)):
                if param[k]["name"] == "safeMoveCheck":
                    device_param = param[k]["deviceParams"]
                    for j in range(len(device_param)):
                        if device_param[j]["key"] == "basic":
                            com = device_param[j]["arrayParam"]["params"]
                            for z in range(len(com)):
                                if com[z]["key"] == "scriptName":
                                    script_name = com[z]["stringValue"]
                                elif com[z]["key"] == "scriptArgs":
                                    script_args = json.loads(com[z]["stringValue"])["operation"]

    if script_name == "ctuNoBlock.py" and script_args == "zero":
        assert True
    elif script_name == "ctuTask.py" and script_args == "robot_reset":
        assert True
    else:
        print(f"script_name : {script_name} and script_args : "
              f"{script_args} is not match")
        assert False


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
