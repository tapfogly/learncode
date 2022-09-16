import math
import sys
import time
import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib
import json

r = rbklib("192.168.9.14", push_flag=True)


def test_safeCheck():
    '''
    料箱车机器人的安全检查
    '''
    # 下载机器人的模型文件
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
                    if param[k]["isEnabled"] == False:
                        print("safeMoveCheck isEnabled is False")
                        assert False
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