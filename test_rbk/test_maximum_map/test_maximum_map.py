import json
import logging
import os
import sys
import time

import pytest

sys.path.append("../..")
from APILib.rbklib import rbklib

ip = "192.168.155.9"


def upload_map_and_do_tasklist(ip: str, map_file: str, map_name: str):
    r1 = rbklib(ip=ip, push_flag=False)
    r1.robot_config_uploadmap_req(map_file)
    time.sleep(2)
    r = rbklib(ip=ip, push_flag=False)
    r.robot_control_loadmap_req(map_name)
    header, body = r.robot_status_reloc_req()
    body = json.loads(body)
    while body["reloc_status"] != 3 and body["reloc_status"] != 1:
        time.sleep(0.1)
        header, body = r.robot_status_reloc_req()
        body = json.loads(body)
    time.sleep(2)
    r.robot_control_comfirmloc_req()
    # send tasklist
    # task = '{"name":"task1","tasks":[{"taskId":0,"desc":"","actionGroups":[{"actions":[{"actionName":"move_action",' \
    #        '"pluginName":"MoveFactory","params":[{"key":"skill_name","stringValue":"GotoSpecifiedPose"},' \
    #        '{"key":"target_name","stringValue":"LM1"}],"ignoreReturn":false,"overtime":0,"externalOverId":-1,' \
    #        '"needResult":false,"sleepTime":0,"actionId":0}],"actionGroupName":"group 1","actionGroupId":0,' \
    #        '"checked":true},{"actions":[{"actionName":"move_action","pluginName":"MoveFactory","params":[{' \
    #        '"key":"skill_name","stringValue":"GotoSpecifiedPose"},{"key":"target_name","stringValue":"LM4"}],' \
    #        '"ignoreReturn":false,"overtime":0,"externalOverId":-1,"needResult":false,"sleepTime":0,"actionId":0}],' \
    #        '"actionGroupName":"group 2","actionGroupId":1,"checked":true},{"actions":[{"actionName":"move_action",' \
    #        '"pluginName":"MoveFactory","params":[{"key":"skill_name","stringValue":"GotoSpecifiedPose"},' \
    #        '{"key":"target_name","stringValue":"LM7"}],"ignoreReturn":false,"overtime":0,"externalOverId":-1,' \
    #        '"needResult":false,"sleepTime":0,"actionId":0}],"actionGroupName":"group 3","actionGroupId":2,' \
    #        '"checked":true},{"actions":[{"actionName":"move_action","pluginName":"MoveFactory","params":[{' \
    #        '"key":"skill_name","stringValue":"GotoSpecifiedPose"},{"key":"target_name","stringValue":"LM10"}],' \
    #        '"ignoreReturn":false,"overtime":0,"externalOverId":-1,"needResult":false,"sleepTime":0,"actionId":0}],' \
    #        '"actionGroupName":"group 4","actionGroupId":3,"checked":true}],"checked":true}],"loop":true} '
    # task = json.loads(task)
    # r.robot_tasklist_req(**task)
    # time.sleep(120)
    # r.robot_tasklist_cancel_req()


def test_large_map():
    maps = [f for f in os.listdir("./maps")]
    maps = sorted(maps, key=lambda x: int(x.split("_")[0]))
    for each_map in maps:
        print("upload map: " + each_map)
        upload_map_and_do_tasklist(ip, os.path.join("./maps", each_map), each_map.split(".smap")[0])
        print("wait......")
        time.sleep(120)


if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
