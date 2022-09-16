import math
import sys
import time
import pytest
import random
sys.path.append("../..")
from APILib.rbklib import rbklib
import json

r = rbklib("192.168.9.14", push_flag=True)


def test_charger():
    """
    检测小车音频功能
    """
    # 查找所有的音频文件
    head, body = r.robot_other_audio_list_req()
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"

    audio = body["audios"]
    if len(audio) == 0:
        print("audio is not exist")
        assert False

    # 随机播放一个音频文件
    head, body = r.robot_other_play_audio_req(audio[random.randint(0, len(audio))])
    body = json.loads(body)
    assert body["ret_code"] == 0, f"{body['err_msg']}"




if __name__ == '__main__':
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
