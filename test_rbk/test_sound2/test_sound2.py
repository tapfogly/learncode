# https://seer-group.coding.net/p/issue_pool/requirements/issues/3332/detail 自动测试用例
# 使用注意： 目前需要手动上传地图和模型文件
# 这个自动化测试用例用于测试，在高级区域播放用户指定的音频，但是当警告和错误发生识别，优先级：指定音频<错误/警告音频

from locale import currency
import pytest
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
p = os.path.dirname(p)
p = os.path.dirname(p)
sys.path.append(p)
from APILib.rbklib import *
import matplotlib.pyplot as plt
RBK = rbklib(getIP()) # 获取机器人IP地址，构造RBK对象

# 前置函数，配置RBK
def setup_module():
    RBK.lock() # 获取控制权
    RBK.robot_config_uploadmap_req(mapPath = "testmap_2.smap") # 上传地图
    RBK.robot_control_loadmap_req(map_name = "testmap_2") # 下载地图
    RBK.robot_config_model_req(modelPath = "WS500-phlips-prototype.model") # 加载机器人模型
    RBK.recoveryParam() # 使用默认参数

def test():
    """高级区域配置 soundName 为 astern 时，遇到障碍物，障碍物再被移开的测试用例
    """
    RBK.cancelTask() # 取消当前任务
    pos = {"x":2.536, "y":9.622, "angle":0}
    RBK.moveRobot(pos) # 移动机器人

    # 增加動態障礙物
    width = 1
    height = 1
    xmid = 15.0 # 障礙物中心橫坐標
    ymid = 3.0  # 障礙物中心縱坐標
    xmin, xmax = xmid - width/2, xmid + width/2
    ymin, ymax = ymid - height/2, ymid + height/2
    RBK.robot_config_addgobstacle_req(
        name =  "obs_a",
        x1 = xmin, 
        y1 = ymin, 
        x2 = xmin, 
        y2 = ymax,
        x3 = xmax, 
        y3 = ymin, 
        x4 = xmax, 
        y4 = ymax)

    # 下發任務
    data = {"id":"LM7"}
    RBK.sendTask(data)

    # 存在障礙物標志
    has_obs = True

    while True:
        time.sleep(0.5)
        current_sname = json.loads(RBK.robot_status_sound_req()[1])["sound_name"]
        pos = RBK.getPos()
        
        # 判斷在高級區域範圍是否播放指定的 astern 音樂
        if (pos["x"] > 4 and pos["x"] < 8) or (pos["x"] > 14 and pos["x"] < 17):
            if current_sname != "astern.wav" and current_sname != "block.wav":
                assert False, "sound name wrong {}".format(current_sname)
        
        # 機器人被阻擋5s移除障礙物
        if current_sname == "block.wav" and has_obs:
            has_obs = False
            time.sleep(5)
            RBK.robot_config_removeobstacle_req() # 移除动态障碍物

        # 判断是否到点
        ts = RBK.getTaskStatus()
        status = ts["task_status"]
        if status == 4:
            assert True
            break

# 测试用例入口
if __name__ == "__main__":
    pytest.main(["--html=report.html", "--self-contained-html"])