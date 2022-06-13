import json


class Test_上传下载地图:
    def test_上传地图(self, rbk):
        head, body = rbk.robot_config_uploadmap_req(r"D:\code\python\AutoTest\TEST_示例\TEST_上传下载地图\testMap.smap")
        body: dict = json.loads(body)
        assert body.get("ret_code") == 0

    def test_下载地图(self, rbk):
        # 地图名是文件内的header中的mapName，不是文件名
        head, body = rbk.robot_config_downloadmap_req("WEIYI-3L")
        body: dict = json.loads(body)
        assert "WEIYI-3L" == body["header"]["mapName"]

    def test_下载一个不存在的地图(self, rbk):
        head, body = rbk.robot_config_downloadmap_req("asdasdasdasd")
        body: dict = json.loads(body)
        assert body.get("ret_code") == 40051