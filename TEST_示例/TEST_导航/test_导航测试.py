import json
import time
import pytest
import xlrd
import sqlite3


# 测试类名，可以将相同的一类测试放在一个测试类里,测试类不能有__init__方法
# 测试类名必须以Test_开头

# 读取文本文件
def textData():
    txt = r"D:\code\python\AutoTest\TEST_示例\TEST_导航\test_data.txt"
    with open(txt, 'r') as f:
        lines = f.readlines()
    return "station", [line.strip() for line in lines]


# 读取excel文件只能是xls格式
def excelData():
    excel = r"D:\code\python\AutoTest\TEST_示例\TEST_导航\test_data.xls"
    lst = []
    # 打开excel文件
    with xlrd.open_workbook(excel) as xls:
        # 获取sheet
        table = xls.sheet_by_name("站点")
        # 获取行数
        for row in range(0, table.nrows):
            # 获取每行第一个单元格的数据
            cell_value = table.cell_value(row, 0)
            lst.append(cell_value)
    return "station", lst


# 读取sqlite数据库
def sqlData():
    db = r"D:\code\python\AutoTest\TEST_示例\TEST_导航\test_data.db"
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("select station from gotarget")
        lst = [line[0] for line in cursor.fetchall()]
    return "station", lst


class Test_导航测试1:
    # 测试方法名，必须以test_开头
    # 使用rbk实例
    @pytest.mark.parametrize(*sqlData())
    def test_导航到站点(self, rbk, station):
        # 返回值为响应头和响应体
        head, body = rbk.robot_task_gotarget_req(id=station)
        # body为bytes格式，转换为(json)字典格式
        body: dict = json.loads(body)
        # 判断执行结果，是否包含错误
        assert body.get("ret_code") == 0

        # 当上一个断言为True时继续执行，否者用例执行失败不执行后续代码

        # 执行检查是否到站点
        isComplete = False
        count = 0
        for i in range(40):
            body = json.loads(rbk.pushData.get())
            print(count, "当前站点:", body.get("current_station"), "任务状态:", body.get("task_status"))
            if body.get("task_status") == 4:
                isComplete = True
                break
            count += 1
            time.sleep(1)
        if not isComplete:
            raise Exception("40秒内未完成任务")
        result = body.get("current_station") == station
        if not result:
            print(f"fatals:{body.get('fatals')}\nerrors:{body.get('errors:')}\nwarnings:{body.get('warnings')}\n")
        assert result

    @pytest.mark.notfind
    def test_导航到一个不存在的站点(self, rbk):
        head, body = rbk.robot_task_gotarget_req(id="LM8888888")
        body: dict = json.loads(body)
        assert body.get("ret_code") == 0
        body = json.loads(rbk.pushData.get())
        result = False
        count = 0
        for i in range(10):
            print(count, "errors:", body.get("errors"))
            if body["errors"][0]["desc"] == "can not find target id LM8888888":
                result = True
                break
            count += 1
            time.sleep(1)
        assert result
