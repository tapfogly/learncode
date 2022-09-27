import math
import sys
import time
import pytest

from APILib.rbklib import rbklib
import json

CarIP = "192.168.9.164"
PluginName = "MultiDcamera"
objModelPath = "tag/t0001.tag"

"""
测试相机识别功能
"""
def test_camera_reconization():
    # 连接小车
    r = rbklib(CarIP, push_flag=True)

    seg_req = {
        "call_pytest": [{
            PluginName: objModelPath
        }]
    }
    _, data = r.request(1851, 1, seg_req)
    response = json.loads(data)['return_data']

    print('response is : ', response)

    if response == '{}':
        print("not get rec result!!!")
    # else:
