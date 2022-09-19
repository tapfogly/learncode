import sys
import math
import pytest
import os

sys.path.append("..")
from APILib.rbklib import rbklib
import json
import time


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
    '''
    查询机器人信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fgqxzx
    '''
    head, body = r.robot_status_info_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_run():
    '''
    查询机器人运行信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/nknw1o
    '''
    head, body = r.robot_status_run_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_loc():
    '''
    查询机器人位置
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/rl3mdn
    '''
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_speed():
    '''
    查询机器人速度
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sv1xwc
    '''
    head, body = r.robot_status_speed_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_block():
    '''
    查询机器人被阻挡状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ih3dxc
    '''
    head, body = r.robot_status_block_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_battery():
    '''
    查询机器人电池状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/vt3ich
    '''
    head, body = r.robot_status_battery_req(simple=False)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_motor():
    '''
    查询电机状态信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/rm6iuu
    '''
    head, body = r.robot_status_motor_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_laser():
    '''
    查询机器人激光点云数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/twtat9
    '''
    head, body = r.robot_status_laser_req(return_beams3D=True)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_area():
    '''
    查询机器人当前所在区域
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/utegst
    '''
    head, body = r.robot_status_area_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_emergency():
    '''
    查询机器人急停状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gd79fw
    '''
    head, body = r.robot_status_emergency_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_io():
    '''
    查询机器人 I/O 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fsd752
    '''
    head, body = r.robot_status_io_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_imu():
    '''
    查询机器人 IMU 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fsd752
    '''
    head, body = r.robot_status_imu_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_rfid():
    '''
    查询 RFID 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/wowmk5
    '''
    head, body = r.robot_status_rfid_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_ultrasonic():
    '''
    查询机器人的超声传感器数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/xgtbks
    '''
    head, body = r.robot_status_ultrasonic_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_pgv():
    '''
    查询二维码数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tdx2gi
    '''
    head, body = r.robot_status_pgv_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_encoder():
    '''
    查询编码器脉冲值
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gs0p35
    '''
    head, body = r.robot_status_encoder_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_task():
    '''
    查询机器人导航状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/eseza1
    '''
    head, body = r.robot_status_task_req(simple=True)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_task_package():
    '''
    查询机器人任务状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/kdurwf
    '''
    d = {
        "task_ids": []
    }
    head, body = r.robot_status_task_status_package_req(d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_reloc():
    '''
    查询机器人当前定位状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sov703
    '''
    head, body = r.robot_status_reloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_loadmap():
    '''
    查询机器人当前地图载入状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/cet2xs
    '''
    head, body = r.robot_status_loadmap_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_slam():
    '''
    查询机器人扫图状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sqmqar
    '''
    head, body = r.robot_status_slam_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_jack():
    '''
    查询顶升机构状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ayhwwz
    '''
    head, body = r.robot_status_jack_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_fork():
    '''
    查询货叉状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/duqu7d
    '''
    head, body = r.robot_status_fork_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_roller():
    '''
    查询辊筒（皮带）状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ehxrcw
    '''
    head, body = r.robot_status_roller_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_dispatch():
    '''
    查询机器人当前调度状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/na7nfm
    '''
    head, body = r.robot_status_dispatch_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_alarm():
    '''
    查询机器人报警状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gbzryy
    '''
    head, body = r.robot_status_alarm_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_all1():
    '''
    查询批量数据 1
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ig6g92
    '''
    head, body = r.robot_status_all1_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_all2():
    '''
    查询批量数据 2
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tvqicn
    '''
    head, body = r.robot_status_all2_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_all3():
    '''
    查询批量数据 3
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/feelog
    '''
    head, body = r.robot_status_all3_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_current_lock():
    '''
    查询当前控制权所有者
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/oik1xw
    '''
    head, body = r.robot_status_current_lock_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_map():
    '''
    查询机器人载入的地图以及储存的地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/plussq
    '''
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_station():
    '''
    查询机器人当前载入地图中的站点信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/cw7dwr
    '''
    head, body = r.robot_status_station()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_mapmd5():
    '''
    查询指定地图列表的MD5值 需要填入查询的地图名字 格式为 地图名 + .smap
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/zk6sug
    '''
    # 查询当前地图
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    current_map = body["current_map"] + ".smap"
    d = {
        "map_names": [current_map]
    }
    head, body = r.robot_status_mapmd5_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_params():
    '''
    查询机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/eazqbb
    '''
    head, body = r.robot_status_params_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_model():
    '''
    下载机器人模型文件
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/upo4w8
    '''
    head, body = r.robot_status_model_req()
    body = json.loads(body)
    assert body["model"] == model_name, f"{body['err_msg']}"


def test_rbk_downloadfile():
    '''
    下载机器人文件
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/efa7zw
    '''
    d = {
        "type": "app",
        "file_path": "rbk.ts"
    }
    head, body = r.robot_status_downloadfile_req(**d)
    try:
        body = json.loads(body)
    except:
        assert True
    else:
        print("ret_code=", body["ret_code"], " err_msg=", body['err_msg'])
        assert False


def test_rbk_canframe():
    '''
    查询驱动器参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/wlw054
    '''
    head, body = r.robot_status_canframe_req()
    body = json.loads(body)
    assert body["ID"] == 0


def test_rbk_transparent():
    '''
    查询透传数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/crqz3f
    '''
    head, body = r.robot_status_transparent_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_gnsscheck():
    '''
    查询GNSS连接状态 id
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lu93rv
    需要小车有 GNSS
    '''
    d = {
        "id": "11"
    }
    head, body = r.robot_status_gnsscheck_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_gnss_list():
    '''
    查询GNSS设备列表
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fgtlbo
    '''
    head, body = r.robot_status_gnsslist_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_rbk_sound():
    '''
    查询当前播放音频名称
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uaeb0b
    '''
    head, body = r.robot_status_sound_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


"""============================================================================
================================= 机器人控制API =================================
============================================================================"""


def test_reloc():
    '''
    小车重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/vw9ixo
    '''

    # 查询小车当前位置
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0

    # 重定位
    x1, y1, angle = body["x"], body["y"], body["angle"]
    d = {
        "x": x1,
        "y": y1,
        "angle": angle
    }
    head, body = r.robot_control_reloc_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0

    '''
    取消重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uos6io
    '''
    time.sleep(1)
    head, body = r.robot_control_cancelreloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    time.sleep(1)
    '''
    确认重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/yotyog
    '''
    head, body = r.robot_control_comfirmloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0


def test_clear_motor():
    '''
    电机编码器标零
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/hnb7da
    '''

    d = {
        "name": "leftrear"
    }
    head, body = r.robot_control_clearmotorencoder_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)
    motor = json.loads(r.pushData.get())["motor_info"]
    for i in range(len(motor)):
        if motor[i]["motor_name"] == "leftrear":
            assert motor[i]["encoder"] == 0


def test_loadmap():
    '''
    切换加载地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/qaga6m
    '''
    # 获取当前地图名
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    global current_map
    current_map = body["current_map"]

    # 获取当前地图以外的地图
    alter_map = None
    for i in range(len(body["maps"])):
        if body["maps"][i] != current_map:
            alter_map = body["maps"][i]
            break

    # 修改地图
    d = {
        "map_name": alter_map
    }
    head, body = r.robot_control_loadmap_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    while True:
        head, body = r.robot_status_loadmap_req()
        if json.loads(body)["loadmap_status"] == 2:
            time.sleep(2)
        elif json.loads(body)["loadmap_status"] == 1:
            break

    time.sleep(1)


def test_uploadmap():
    '''
    从机器人下载地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/kwdo4y
    '''
    global current_map
    # 下载当前地图
    with open(current_map, "w") as f:
        map_head, map_body = r.robot_config_downloadmap_req(current_map)
        map_body = json.loads(map_body)
        f.write(json.dumps(map_body, separators=(",", ":")))

    '''
    上传并切换小车地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lzhqo5
    '''
    head, body = r.robot_config_upload_and_loadmap_req(current_map)
    body = json.loads(body)
    assert body["ret_code"] == 0

    while True:
        head, body = r.robot_status_loadmap_req()
        if json.loads(body)["loadmap_status"] == 1:
            break
        time.sleep(1)

    # 确认重定位
    head, body = r.robot_control_comfirmloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    time.sleep(2)


"""============================================================================
================================= 机器人配置API =================================
============================================================================"""


def test_upload():
    '''
    上传地图到机器人
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gswi7g
    '''
    # 获取当前地图名
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    current_map = body["current_map"]

    # 上传地图
    head, body = r.robot_config_uploadmap_req(current_map)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_src():
    '''
    src 控制模式
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fb2yrb
    '''
    head, body = r.robot_config_src_require_req()
    body = json.loads(body)

    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_src_release():
    '''
    src 监听模式
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/pvx0z4
    '''
    head, body = r.robot_config_src_require_req()
    body = json.loads(body)

    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_set_clear_error():
    '''
    设置第三方 Error
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gawl3t
    '''

    msg = "test a error"
    head, body = r.robot_config_seterror_req(msg)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    '''
    清除第三方 Error
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/guw3ee
    '''
    time.sleep(4)

    head, body = r.robot_config_clearerror_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_set_clear_warning():
    '''
    设置第三方 Waring
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/knkh26
    '''

    msg = "test a warning"
    head, body = r.robot_config_setwarning_req(msg)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(4)
    '''
    清除第三方 Waring
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ntinqh
    '''
    head, body = r.robot_config_clearwarning_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_setparams():
    '''
    临时修改机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ia23vg
    '''

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    default_name = body["NetProtocol"]["RobotName"]["value"]
    print(default_name)
    name = "test_name"
    d = {
        "NetProtocol": {
            "RobotName": name
        }
    }
    head, body = r.robot_config_setparams_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    assert body["NetProtocol"]["RobotName"]["value"] == name

    '''
    恢复机器人参数为默认值
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/de8zrk
    '''
    d = [{
        "params": ["RobotName"],
        "plugin": "NetProtocol"
    }]
    head, body = r.robot_config_reloadparams_req(d)
    body = json.loads(body)
    time.sleep(4)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    assert body["NetProtocol"]["RobotName"]["value"] == default_name


def test_saveparams():
    '''
    永久修改机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ngzl6m
    '''

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    default_name = body["NetProtocol"]["RobotName"]["value"]

    # 永久修改机器人参数
    name = "test_name"
    d = {
        "NetProtocol": {
            "RobotName": name
        }
    }
    head, body = r.robot_config_saveparams_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(2)

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    assert body["NetProtocol"]["RobotName"]["value"] == name

    time.sleep(2)

    # 恢复原本参数
    d = {
        "NetProtocol": {
            "RobotName": default_name
        }
    }
    head, body = r.robot_config_saveparams_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(2)

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    assert body["NetProtocol"]["RobotName"]["value"] == default_name


def test_obstacle():
    '''
    动态障碍物相关测试

    世界坐标系插入动态障碍物
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gu125z
    '''

    name = "test_obstacle"
    x1, y1 = 1.5, 0.5
    x2, y2 = 1, 0.5
    x3, y3 = 1.5, -0.5
    x4, y4 = 1, -0.5
    head, body = r.robot_config_addgobstacle_req(name, x1, y1, x2, y2, x3, y3, x4, y4)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    # 查询动态障碍点
    user_obj = json.loads(r.pushData.get())["user_objects"]
    assert user_obj[0]["name"] == name

    time.sleep(1)

    # 删除动态障碍点
    head, body = r.robot_config_removeobstacle_req(name)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    '''
    机器人坐标系下插入动态障碍物
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/frf64h
    '''
    time.sleep(2)

    x1, y1 = 1.5, 0.5
    x2, y2 = 1, 0.5
    x3, y3 = 1.5, -0.5
    x4, y4 = 1, -0.5
    head, body = r.robot_config_addobstacle_req(name, x1, y1, x2, y2, x3, y3, x4, y4)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    user_obj = json.loads(r.pushData.get())["user_objects"]
    assert user_obj[0]["name"] == name

    time.sleep(1)

    head, body = r.robot_config_removeobstacle_req(name)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_clear_all_err():
    '''
    清除所有的错误信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/dwghi4
    '''

    for i in range(5):
        msg = "test a error " + str(i)
        head, body = r.robot_config_seterror_req(msg)
        body = json.loads(body)
        assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(3)

    head, body = r.robot_config_clearallerrors_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_motor():
    '''
    电机清错
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uq1p6u
    '''

    name = "motor1"
    head, body = r.robot_config_motor_clear_fault_req(name)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


"""============================================================================
================================= 机器人其它API =================================
============================================================================"""


def test_peripheral_data():
    '''
    写入外设用户自定义数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/pzzf6k
    '''

    head, body = r.robot_other_write_peripheral_data_req(id=0, data=233)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_update_transparent():
    '''
    更新透传数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tqtvwm
    '''
    d = {
        "1": "test"
    }
    head, body = r.robot_other_update_transparent_data_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_softemc():
    '''
    软急停
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ostqp6
    '''

    status = True
    head, body = r.robot_other_softemc_req(status=status)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    head, body = r.robot_status_emergency_req()
    body = json.loads(body)
    assert status == body["soft_emc"]

    head, body = r.robot_other_softemc_req(status=False)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def test_audio():
    '''
    播放音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    '''
    head, body = r.robot_other_play_audio_req("navigation", True)
    body = json.loads(body)
    assert body["ret_code"] == 0

    time.sleep(2)
    '''
    暂停音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    '''
    head, body = r.robot_other_pause_audio_req()
    body = json.loads(body)
    assert body["ret_code"] == 0

    # 播放音频
    head, body = r.robot_other_play_audio_req("navigation", True)
    body = json.loads(body)
    assert body["ret_code"] == 0

    time.sleep(2)

    '''
    停止音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    '''
    head, body = r.robot_other_stop_audio_req()
    body = json.loads(body)
    assert body["ret_code"] == 0


"""============================================================================
================================= 机器人导航API =================================
============================================================================"""


def test_precision():
    '''
    运动到点精度
    '''
    r = rbklib(ip, push_flag=True)
    r.robot_control_comfirmloc_req()

    d = {
        "source_id": source_id,
        "id": task,
        "task_id": "test_amb300"
    }

    head, body = r.robot_task_gotarget_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    '''
    查看机器人导航状态
    '''
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

    '''
    获取机器人当前的位置信息
    '''
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x1, y1 = body["x"], body["y"]
    print("x1 = ", x1, " y1", y1)
    '''
    查询目标点信息
    '''
    head, body = r.robot_status_station()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"
    x2, y2 = None, None
    for i in range(len(body["stations"])):
        if body["stations"][i]["id"] == task:
            x2 = body["stations"][i]["x"]
            y2 = body["stations"][i]["y"]

    assert 0.01 >= abs(x2 - x1) and 0.01 >= abs(y2 - y1)


def test_robot_turn():
    '''
    转动
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ck7o3v
    '''

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

    new_rad = json.loads(r.pushData.get())["angle"]
    abs_angle = abs(new_rad - old_rad)
    if new_rad > math.pi:
        abs_angle = 2 * math.pi - abs_angle
    if rad > math.pi:
        abs_angle = 2 * math.pi - abs_angle
    assert -0.017 < abs_angle - rad < 0.017


def test_robot_translate():
    '''
    平动
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lz24sz
    '''

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
    '''
    测试小车充电模型文件配置
    '''
    r = rbklib(ip)
    r.lock()
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


"""=============================================================================
===============================子项目测试=========================================
============================================================================="""


def test_jack_height():
    '''
    检查顶升高度
    '''

    head, body = r.robot_status_model_req()
    body = json.loads(body)
    device_type = body["deviceTypes"]

    ok = True
    for i in range(len(device_type)):
        if device_type[i]["name"] == "jack":
            param = device_type[i]["devices"]
            for k in range(len(param)):
                if param[k]["name"] == "jack":
                    device_param = param[k]["deviceParams"]
                    for j in range(len(device_param)):
                        if device_param[j]["key"] == "type":
                            com = device_param[j]["comboParam"]["childParams"]
                            for z in range(len(com)):
                                if com[z]["key"] == "byDO":
                                    param = com[z]["params"]
                                    for w in range(len(param)):
                                        if param[w]["key"] == "maxHeight":
                                            if param[w]["doubleValue"] >= 0.06:
                                                # param[w]["doubleValue"] = 0.05
                                                # ok = False
                                                assert False
                                            else:
                                                assert True



def test_rssi():
    '''
    获取网络信息强度
    '''
    rssi_value = json.loads(r.pushData.get())["rssi"]
    dbm = rssi_value - 100
    assert dbm >= -65, "网络信号强度低于-65"


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
