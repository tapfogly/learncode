import json
import time


def rbk_info(r):
    """
    查询机器人信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fgqxzx
    """
    head, body = r.robot_status_info_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_run(r):
    """
    查询机器人运行信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/nknw1o
    """
    head, body = r.robot_status_run_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_loc(r):
    """
    查询机器人位置
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/rl3mdn
    """
    head, body = r.robot_status_loc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_speed(r):
    """
    查询机器人速度
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sv1xwc
    """
    head, body = r.robot_status_speed_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_block(r):
    """
    查询机器人被阻挡状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ih3dxc
    """
    head, body = r.robot_status_block_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_battery(r):
    """
    查询机器人电池状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/vt3ich
    """
    head, body = r.robot_status_battery_req(simple=False)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_motor(r):
    """
    查询电机状态信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/rm6iuu
    """
    head, body = r.robot_status_motor_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_laser(r):
    """
    查询机器人激光点云数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/twtat9
    """
    head, body = r.robot_status_laser_req(return_beams3D=True)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_area(r):
    """
    查询机器人当前所在区域
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/utegst
    """
    head, body = r.robot_status_area_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_emergency(r):
    """
    查询机器人急停状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gd79fw
    """
    head, body = r.robot_status_emergency_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_io(r):
    """
    查询机器人 I/O 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fsd752
    """
    head, body = r.robot_status_io_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_imu(r):
    """
    查询机器人 IMU 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fsd752
    """
    head, body = r.robot_status_imu_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_rfid(r):
    """
    查询 RFID 数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/wowmk5
    """
    head, body = r.robot_status_rfid_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_ultrasonic(r):
    """
    查询机器人的超声传感器数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/xgtbks
    """
    head, body = r.robot_status_ultrasonic_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_pgv(r):
    """
    查询二维码数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tdx2gi
    """
    head, body = r.robot_status_pgv_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_encoder(r):
    """
    查询编码器脉冲值
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gs0p35
    """
    head, body = r.robot_status_encoder_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_task(r):
    """
    查询机器人导航状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/eseza1
    """
    head, body = r.robot_status_task_req(simple=True)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_task_package(r):
    """
    查询机器人任务状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/kdurwf
    """
    d = {
        "task_ids": []
    }
    head, body = r.robot_status_task_status_package_req(d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_reloc(r):
    """
    查询机器人当前定位状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sov703
    """
    head, body = r.robot_status_reloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_loadmap(r):
    """
    查询机器人当前地图载入状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/cet2xs
    """
    head, body = r.robot_status_loadmap_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_slam(r):
    """
    查询机器人扫图状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/sqmqar
    """
    head, body = r.robot_status_slam_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_jack(r):
    """
    查询顶升机构状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ayhwwz
    """
    head, body = r.robot_status_jack_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_fork(r):
    """
    查询货叉状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/duqu7d
    """
    head, body = r.robot_status_fork_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_roller(r):
    """
    查询辊筒（皮带）状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ehxrcw
    """
    head, body = r.robot_status_roller_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_dispatch(r):
    """
    查询机器人当前调度状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/na7nfm
    """
    head, body = r.robot_status_dispatch_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_alarm(r):
    """
    查询机器人报警状态
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gbzryy
    """
    head, body = r.robot_status_alarm_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_all1(r):
    """
    查询批量数据 1
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ig6g92
    """
    head, body = r.robot_status_all1_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_all2(r):
    """
    查询批量数据 2
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tvqicn
    """
    head, body = r.robot_status_all2_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_all3(r):
    """
    查询批量数据 3
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/feelog
    """
    head, body = r.robot_status_all3_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_current_lock(r):
    """
    查询当前控制权所有者
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/oik1xw
    """
    head, body = r.robot_status_current_lock_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_map(r):
    """
    查询机器人载入的地图以及储存的地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/plussq
    """
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_station(r):
    """
    查询机器人当前载入地图中的站点信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/cw7dwr
    """
    head, body = r.robot_status_station()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_mapmd5(r):
    """
    查询指定地图列表的MD5值 需要填入查询的地图名字 格式为 地图名 + .smap
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/zk6sug
    """
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


def rbk_params(r):
    """
    查询机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/eazqbb
    """
    head, body = r.robot_status_params_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_model(r, model_name):
    """
    下载机器人模型文件
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/upo4w8
    """
    head, body = r.robot_status_model_req()
    body = json.loads(body)
    assert body["model"] == model_name, f"{body['err_msg']}"


def rbk_downloadfile(r):
    """
    下载机器人文件
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/efa7zw
    """
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


def rbk_canframe(r):
    """
    查询驱动器参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/wlw054
    """
    head, body = r.robot_status_canframe_req()
    body = json.loads(body)
    assert body["ID"] == 0


def rbk_transparent(r):
    """
    查询透传数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/crqz3f
    """
    head, body = r.robot_status_transparent_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_gnsscheck(r):
    """
    查询GNSS连接状态 id
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lu93rv
    需要小车有 GNSS
    """
    d = {
        "id": "11"
    }
    head, body = r.robot_status_gnsscheck_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_gnss_list(r):
    """
    查询GNSS设备列表
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fgtlbo
    """
    head, body = r.robot_status_gnsslist_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def rbk_sound(r):
    """
    查询当前播放音频名称
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uaeb0b
    """
    head, body = r.robot_status_sound_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


"""============================================================================
================================= 机器人控制API =================================
============================================================================"""


def reloc(r):
    """
    小车重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/vw9ixo
    """

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

    """
    取消重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uos6io
    """
    time.sleep(1)
    head, body = r.robot_control_cancelreloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    time.sleep(1)
    """
    确认重定位
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/yotyog
    """
    head, body = r.robot_control_comfirmloc_req()
    body = json.loads(body)
    assert body["ret_code"] == 0


def clear_motor(r):
    """
    电机编码器标零
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/hnb7da
    """

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


def loadmap(r):
    """
    切换加载地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/qaga6m
    """
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


def uploadmap(r):
    """
    从机器人下载地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/kwdo4y
    """
    global current_map
    # 下载当前地图
    with open(current_map, "w") as f:
        map_head, map_body = r.robot_config_downloadmap_req(current_map)
        map_body = json.loads(map_body)
        f.write(json.dumps(map_body, separators=(",", ":")))

    """
    上传并切换小车地图
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/lzhqo5
    """
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


def upload(r):
    """
    上传地图到机器人
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gswi7g
    """
    # 获取当前地图名
    head, body = r.robot_status_map_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
    current_map = body["current_map"]

    # 上传地图
    head, body = r.robot_config_uploadmap_req(current_map)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def src(r):
    """
    src 控制模式
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/fb2yrb
    """
    head, body = r.robot_config_src_require_req()
    body = json.loads(body)

    assert body["ret_code"] == 0, f"{body['err_msg']}"


def src_release(r):
    """
    src 监听模式
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/pvx0z4
    """
    head, body = r.robot_config_src_require_req()
    body = json.loads(body)

    assert body["ret_code"] == 0, f"{body['err_msg']}"


def set_clear_error(r):
    """
    设置第三方 Error
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gawl3t
    """

    msg = "test a error"
    head, body = r.robot_config_seterror_req(msg)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    """
    清除第三方 Error
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/guw3ee
    """
    time.sleep(4)

    head, body = r.robot_config_clearerror_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def set_clear_warning(r):
    """
    设置第三方 Waring
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/knkh26
    """

    msg = "test a warning"
    head, body = r.robot_config_setwarning_req(msg)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(4)
    """
    清除第三方 Waring
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ntinqh
    """
    head, body = r.robot_config_clearwarning_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def setparams(r):
    """
    临时修改机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ia23vg
    """

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    default_name = body["NetProtocol"]["RobotName"]["value"]
    print(default_name)
    name = "name"
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

    """
    恢复机器人参数为默认值
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/de8zrk
    """
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


def saveparams(r):
    """
    永久修改机器人参数
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ngzl6m
    """

    # 查询机器人参数
    head, body = r.robot_status_params_req("NetProtocol", "RobotName")
    body = json.loads(body)
    default_name = body["NetProtocol"]["RobotName"]["value"]

    # 永久修改机器人参数
    name = "name"
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


def obstacle(r):
    """
    动态障碍物相关测试

    世界坐标系插入动态障碍物
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/gu125z
    """

    name = "obstacle"
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

    """
    机器人坐标系下插入动态障碍物
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/frf64h
    """
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


def clear_all_err(r):
    """
    清除所有的错误信息
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/dwghi4
    """

    for i in range(5):
        msg = "test a error " + str(i)
        head, body = r.robot_config_seterror_req(msg)
        body = json.loads(body)
        assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(3)

    head, body = r.robot_config_clearallerrors_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def motor(r):
    """
    电机清错
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/uq1p6u
    """

    name = "motor1"
    head, body = r.robot_config_motor_clear_fault_req(name)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


"""============================================================================
================================= 机器人其它API =================================
============================================================================"""


def peripheral_data(r):
    """
    写入外设用户自定义数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/pzzf6k
    """

    head, body = r.robot_other_write_peripheral_data_req(id=0, data=233)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def update_transparent(r):
    """
    更新透传数据
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/tqtvwm
    """
    d = {
        "1": "test"
    }
    head, body = r.robot_other_update_transparent_data_req(**d)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def softemc(r):
    """
    软急停
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/ostqp6
    """

    status = True
    head, body = r.robot_other_softemc_req(status=status)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    time.sleep(1)

    head, body = r.robot_status_emergency_req()
    body = json.loads(body)
    assert status == body["soft_emc"]

    head, body = r.robot_other_softemc_req(status=False)
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"


def audio(r):
    """
    播放音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    """
    head, body = r.robot_other_play_audio_req("navigation", True)
    body = json.loads(body)
    assert body["ret_code"] == 0

    time.sleep(2)
    """
    暂停音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    """
    head, body = r.robot_other_pause_audio_req()
    body = json.loads(body)
    assert body["ret_code"] == 0

    # 播放音频
    head, body = r.robot_other_play_audio_req("navigation", True)
    body = json.loads(body)
    assert body["ret_code"] == 0

    time.sleep(2)

    """
    停止音频
    接口详情 https://seer-group.yuque.com/pf4yvd/ruzsiq/axin2t
    """
    head, body = r.robot_other_stop_audio_req()
    body = json.loads(body)
    assert body["ret_code"] == 0
