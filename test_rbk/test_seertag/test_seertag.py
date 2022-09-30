import base64
import json

import cv2
import numpy as np
from APILib.rbklib import getIP, rbklib
import time

# 插件名称
PluginName = "IRCameraPose"
def send_req(rbk, req: dict) -> dict:
    """发送请求
    rbk: rbklib实例
    req: 待发送的请求

    return: 请求的应答
    """
    # 准备请求的数据
    seertag_req = {
        "call_pytest": [{
            PluginName: req
        }]
    }
    # 发送pytest请求
    _, data = rbk.request(1851, 1, seertag_req)
    # 获取返回值
    response = json.loads(data)['return_data']
    return json.loads(response)
def test_seertag():
    # 连接rbk
    rbk = rbklib(getIP())
    check_model = "basic_model"
    if check_model == "basic_model":
        # 查询启用的设备个数
        response = send_req(rbk, {'cmd': 0})
        print(response)
        # 确认应答正确
        if response.get("seertag_family_id") == 1:
            print("seer tag family is set correctly")
        else:
            print(" seertag_family_id ERROR")
        if response.get("infrared"):
            print("Open infrared camera successfully")
        else:
            print("Failed to turn on the infrared camera")
        if response.get("seertag_size") == 0.02:
            print("seer tag size setting: 0.02")
        else:
            print("seer tag size setting failed")

        # # 开启二维码检测
        response = send_req(rbk, {'cmd': 1})
        # # 确认应答正确
        print(response)
        if response.get("detector_status"):
            print("Successfully detected seertag detector")
        else:
            print("Failed to open seer tag detector")
        time.sleep(2)

        # 关闭二维码检测
        response = send_req(rbk, {'cmd': 2})
        # 确认应答正确
        if response.get("detector_status"):
            print("seer tag detector closed successfully")
        else:
            print("seer tag detector closing failed")
        time.sleep(2)

        # 开启二维码建图
        response = send_req(rbk, {'cmd': 3})
        # 确认应答正确

        if response.get("slam_status"):
            print("seer tag mapping opened successfully")
        else:
            print("failed to open seer tag mapping")
        time.sleep(2)
        # 关闭二维码建图
        response = send_req(rbk, {'cmd': 4})
        if response.get("slam_status"):
            print("seertag  mapping closed successfully")
        else:
            print("failed to close seer tag mapping")

        # 检查图像传输是否正常
        response = send_req(rbk, {'cmd': 5})
        # 确认应答正确
        if response.get("video_status"):
            print("Image transmission is ok")
        else:
            print("Problem in image transmission")
    if check_model == "advanced_model":
        # 检查是否可以检测到二维码
        response = send_req(rbk, {'cmd': 6})
        # 确认应答正确
        if response.get("find_tags"):
            print("find seer tag")
        else:
            print(" not find seer tag")
    if check_model == "image_model":
         # 检查图像数据
        response = send_req(rbk, {'cmd': 7})
        if response.get('img') == "error":
            print("no image")
        res = base64.b64decode(response.get('img'))
        arr = np.frombuffer(res, np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        cv2.imshow('TEST_SEER_TAG_PHOTO', image)
        cv2.waitKey(0)
