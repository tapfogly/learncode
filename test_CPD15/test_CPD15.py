import sys
import math
import pytest
import paramiko

sys.path.append("..")
from APILib.rbklib import rbklib
from APILib.robodLib import RobodLib
from APILib.common import *


def setup_module():
    open_ip = None
    model = None
    s_id = None
    task_id = None
    charger_name = None
    vol = None
    user_name = None
    pwd = None
    with open("config.json", "r") as f:
        body = json.loads(f.read())
        open_ip = body["ip"]
        model = body["model_name"]
        s_id = body["source_id"]
        task_id = body["id"]
        charger_name = body["charger_name"]
        vol = body["volume"]
        user_name = body["user_name"]
        pwd = body["pwd"]
    return open_ip, model, s_id, task_id, charger_name, vol, user_name, pwd


ip, model_name, source_id, task, charger, volume, user_name, pwd = setup_module()
r = rbklib(ip, push_flag=True)
r.robot_config_lock_req("test_robot")
current_map: str = ""
file_path = "/usr/local/etc/.SeerRobotics/rbk/resources/models/robot.cp"
rod = RobodLib(ip)


def teardown_module():
    unlock(r)


"""============================================================================
================================= 机器人状态API =================================
============================================================================"""


class Test_机器人状态:
    def test_信息(self):
        rbk_info(r)

    def test_运行信息(self):
        rbk_run(r)

    def test_位置(self):
        rbk_loc(r)

    def test_速度(self):
        rbk_speed(r)

    def test_被阻挡状态(self):
        rbk_block(r)

    def test_电池状态(self):
        rbk_battery(r)

    def test_点击状态(self):
        rbk_motor(r)

    def test_激光点云(self):
        rbk_laser(r)

    def test_当前区域(self):
        rbk_area(r)

    def test_急停状态(self):
        rbk_emergency(r)

    def test_io数据(self):
        rbk_io(r)

    def test_imu数据(self):
        rbk_imu(r)

    def test_rfid数据(self):
        rbk_rfid(r)

    def test_超声数据(self):
        rbk_ultrasonic(r)

    def test_二维码数据(self):
        rbk_pgv(r)

    def test_编码器脉冲值(self):
        rbk_encoder(r)

    def test_导航状态(self):
        rbk_task(r)

    def test_任务状态(self):
        rbk_task_package(r)

    def test_定位状态(self):
        rbk_reloc(r)

    def test_地图载入状态(self):
        rbk_loadmap(r)

    def test_扫图状态(self):
        rbk_slam(r)

    def test_顶升机构状态(self):
        rbk_jack(r)

    def test_货叉状态(self):
        rbk_fork(r)

    def test_辊筒状态(self):
        rbk_roller(r)

    def test_调度状态(self):
        rbk_dispatch(r)

    def test_报警状态(self):
        rbk_alarm(r)

    def test_批量数据1(self):
        rbk_all1(r)

    def test_批量数据2(self):
        rbk_all2(r)

    def test_批量数据3(self):
        rbk_all3(r)

    def test_控制权所属(self):
        rbk_current_lock(r)

    def test_当前地图和地图列表(self):
        rbk_map(r)

    def test_当前地图站点信息(self):
        rbk_station(r)

    def test_地图MD5值(self):
        rbk_mapmd5(r)

    def test_机器人参数(self):
        rbk_params(r)

    def test_下载模型文件(self):
        rbk_model(r, model_name)

    def test_下载机器人文件(self):
        rbk_downloadfile(r)

    def test_驱动器参数(self):
        rbk_canframe(r)

    def test_透传数据(self):
        rbk_transparent(r)

    def test_gnss连接状态(self):
        rbk_gnsscheck(r)

    def test_gnss设备列表(self):
        rbk_gnss_list(r)

    def test_当前播放音频(self):
        rbk_sound(r)


"""============================================================================
================================= 机器人控制API =================================
============================================================================"""


class Test_控制:
    def test_小车重定位(self):
        reloc(r)

    def test_编码器标零(self):
        clear_motor(r)

    def test_切换加载地图(self):
        loadmap(r)

    def test_上传并切换地图(self):
        uploadmap(r)


"""============================================================================
================================= 机器人配置API =================================
============================================================================"""


class Test_配置:

    def test_上传地图(self):
        upload(r)

    def test_src控制模式(self):
        src(r)

    def test_src监听模式(self):
        src_release(r)

    def test_设置并清除错误(self):
        set_clear_error(r)

    def test_设置并清除警告(self):
        set_clear_warning(r)

    def test_临时修改机器人参数(self):
        setparams(r)

    def test_永久修改机器人参数(self):
        saveparams(r)

    def test_插入和清除障碍物(self):
        obstacle(r)

    def test_清除所有错误(self):
        clear_all_err(r)

    def test_电机清错(self):
        motor(r)


"""============================================================================
================================= 机器人其它API =================================
============================================================================"""


class Test_其它:
    def test_写入外设自定义数据(self):
        peripheral_data(r)

    def test_更新透传数据(self):
        update_transparent(r)

    def test_软急停(self):
        softemc(r)

    def test_音频(self):
        audio(r)


"""============================================================================
================================= 机器人导航API =================================
============================================================================"""


class Test_导航:

    def test_到位精度(self):
        """
        运动到点精度
        """
        time.sleep(2)

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

    def test_转动(self):
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

    def test_平动(self):
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


class Test_拓展:
    def test_模型文件充电参数检查(self):
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

    def test_充电检查(self):
        """
        充电检查
        """
        # 去充电桩
        d = {
            "id": charger
        }
        head, body = r.robot_task_gotarget_req(**d)
        body = json.loads(body)
        assert body["ret_code"] == 0

        start = time.time()
        while True:
            end = time.time()
            body = json.loads(r.pushData.get())
            if body["task_status"] == 2:
                time.sleep(1)
            elif body["task_status"] == 4:
                break

        # 离开充电桩
        d = {
            "id": source_id
        }
        head, body = r.robot_task_gotarget_req(**d)
        body = json.loads(body)
        assert body["ret_code"] == 0

        start = time.time()
        while True:
            end = time.time()
            body = json.loads(r.pushData.get())
            if end - start >= 300:
                break
            elif body["task_status"] == 2:
                time.sleep(1)
            elif body["task_status"] == 4:
                break

        time.sleep(1)

        # 查询充电状态
        head, body = r.robot_status_battery_req()
        body = json.loads(body)
        assert body["ret_code"] == 0

        # 如果离开充电桩仍充电那么存在问题
        if not body["charging"]:
            assert True
        else:
            assert False

    def test_标定(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username=user_name, password=pwd)

        stdin, stdout, stderr = ssh.exec_command(f"cat {file_path}")
        data = json.loads(stdout.read())
        ssh.close()
        laser_status = False
        if data is {}:
            print("小车未标定")
            assert False
        else:
            if data["deviceTypes"]:
                device = data["deviceTypes"]
                for i in device:
                    if i.get("name") == "laser":
                        device = i["devices"]
                        for j in device:
                            if j.get("name") == "laser":
                                laser_status = analysis_laser(j["deviceParams"][0])
            else:
                print("json 数据异常")
                assert False
        assert laser_status

    def test_音量调控(self):
        head, body = rod.robot_core_setvolumelevel_req("", volume=volume)
        body = json.loads(body)
        assert body["volume"] == volume

    def test_对时(self):
        head, body = rod.request(5117, 1)
        body = json.loads(body)
        data_time = body["dateTime"]
        data_time = data_time.rsplit(':')[0] + ':' + data_time.rsplit(':')[1] + ':' \
                    + data_time.rsplit(':')[2]
        timestamp = time.mktime(time.strptime(str(data_time), "%Y-%m-%d %H:%M:%S"))
        if time.time() - timestamp >= 500:
            assert False
        assert True

    def test_货叉精度(self):
        height = 0.5
        head, body = r.robot_other_set_fork_height_req(height)
        body = json.loads(body)
        assert body["ret_code"] == 0

        start = time.time()
        while True:
            head, body = r.robot_status_task_req()
            body = json.loads(body)
            if time.time() - start >= 30:
                break
            elif body["task_status"] == 2:
                time.sleep(1)
                continue
            elif body["task_status"] == 4:
                break

        head, body = r.robot_status_fork_req()
        body = json.loads(body)

        assert height - 0.01 <= body["fork_height"] <= height + 0.01

    def test_运行中货叉精度(self):
        fork_mid_height = 0.6
        cmd = {
            "id": task,
            "source_id": source_id,
            "operation": "ForkHeight",
            "fork_mid_height": fork_mid_height
        }
        head, body = r.robot_task_gotarget_req(**cmd)
        body = json.loads(body)
        assert body["ret_code"] == 0

        start = time.time()
        while True:
            head, body = r.robot_status_task_req()
            body = json.loads(body)
            if time.time() - start >= 30:
                break
            elif body["task_status"] == 2:
                time.sleep(1)
                continue
            elif body["task_status"] == 4:
                break

        head, body = r.robot_status_fork_req()
        body = json.loads(body)

        assert fork_mid_height - 0.01 <= body["fork_height"] <= fork_mid_height + 0.01


def analysis_laser(value):
    value = value["arrayParam"]["params"]
    for i in value:
        if abs(i["doubleValue"]) > 0.018:
            print(f"laser calib {i['key']} is {i['doubleValue']}")
            return False
    return True


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
