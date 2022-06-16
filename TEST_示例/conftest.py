import datetime
from _pytest.nodes import Item
from py.xml import html
import os
import sys
import time
import configparser
import webbrowser
import pytest
from _pytest.config import ExitCode

sys.path.append("..")
from APILib.codingLib import CodingLib
from APILib.rbklib import rbklib

########################################################################################################################
#                                                                                                                      #
#                                                 下面是 Hook                                                           #
#                                                                                                                      #
########################################################################################################################

# 增加命令行参数
def pytest_addoption(parser):
    """
    添加命令行参数\n
    --title: 指定报告标题\n
    --tester: 指定测试者姓名\n
    --client-id: 指定CODING OAuth2.0 ID\n
    --client-secret: CODING OAuth2.0 密钥\n
    --token: 指定CODING 个人授权令牌\n
    --enable-coding: 启用 CODING 上传测试报告\n
    """
    group = parser.getgroup("seer")
    group.addoption("--title", help="报告标题")
    group.addoption("--tester", help="测试者姓名")
    group.addoption("--client-id", help="CODING OAuth2.0 ID")
    group.addoption("--client-secret", help="CODING OAuth2.0 密钥")
    group.addoption("--token", help="CODING 个人授权令牌")
    group.addoption("--enable-coding", action="store_true", help="是否启用CODING")


# 会话开始前，检查命令行参数，记录时间，创建 CODING 实例
def pytest_sessionstart(session):
    global cfgExist
    global title
    global tester
    global cf
    global startTime
    global coding
    title = session.config.getoption("--title")
    tester = session.config.getoption("--tester")
    # 判断配置文件是否存在
    cfgExist = os.path.exists("config.ini")
    if cfgExist:
        cf = configparser.ConfigParser()
        cf.read("config.ini", encoding="utf-8")
    # 报告标题
    if not title and cfgExist:
        title = cf["MetaData"]["Title"]
    else:
        title = "Test Report"
    # 测试者姓名
    if not tester and cfgExist:
        tester = cf["MetaData"]["Tester"]
    if not session.config.getoption("--enable-coding"):
        return
    token = session.config.getoption("--token")
    client_id = session.config.getoption("--client-id")
    client_secret = session.config.getoption("--client-secret")
    if not token and not (client_id and client_secret) and cfgExist:
        token = cf["CODING"]["Token"]
        client_id = cf["CODING"]["ClientId"]
        client_secret = cf["CODING"]["ClientSecret"]
    # 记录测试开始时间
    startTime = time.time()
    # 判断是否指定了CODING OAuth2.0 ID、密钥、令牌，创建 CODING 实例
    if token:
        coding = CodingLib(token)
    elif client_id and client_secret:
        coding = CodingLib(client_id, client_secret)
    else:
        coding = None


# 会话结束后，上传 CODING 打开报告
def pytest_sessionfinish(session, exitstatus):
    report = session.config.getoption("--html")
    if report:
        webbrowser.open(report)
    # 如果没有启用CODING，则不上传测试报告
    if not session.config.getoption("--enable-coding"):
        return
    if coding and cfgExist and report and (exitstatus == ExitCode.OK or exitstatus == ExitCode.TESTS_FAILED):
        testPassed = session.testscollected - session.testsfailed
        data = session.config._metadata
        # 评论或创建事项的数据，通过、失败、通过率、测试时间
        data.update({"Passed": testPassed
                     , "Failed": session.testsfailed
                     , "SuccessRate": f"{testPassed / session.testscollected * 100:.2f} %"
                     , "Duration": f"{time.time() - startTime:.2f} s"
                     , "Tester": tester})
        # 创建事项
        if cf["CODING"]["IssueMethod"] == "Create":
            md = coding.generateMarkdown(title, cf["Create"]["Description"], data)
            projectName = cf["Create"]["ProjectName"]
            issueType = cf["Create"]["Type"]
            name = cf["Create"]["Name"] if cf["Create"]["Name"] else title
            priority = cf["Create"]["Priority"]
            startDate = cf["Create"]["StartDate"] if cf["Create"]["StartDate"] else datetime.date.today()
            dueDate = cf["Create"]["DueDate"] if cf["Create"]["DueDate"] else datetime.date.today() + datetime.timedelta(days=7)
            assigneeId = cf["Create"].getint("AssigneeId")
            watcherIds = [int(id) for id in cf["Create"]["WatcherIds"].split()]
            d = {"Description": md}
            if assigneeId:
                d["AssigneeId"] = assigneeId
            if watcherIds:
                d["WatcherIds"] = watcherIds
            res = coding.createIssue(projectName, issueType, name, priority, startDate, dueDate, **d)
            print(res.text)
        # 评论事项
        elif cf["CODING"]["IssueMethod"] == "Comment":
            md = coding.generateMarkdown(title, cf["Comment"]["Content"], data)
            projectName = cf["Comment"]["ProjectName"]
            issueCode = cf["Comment"].getint("IssueCode")
            res = coding.createIssueComment(projectName, issueCode, md)
            print(res.text)


def pytest_collection_modifyitems(session, config, items: list):
    """ 收集测试用例后被调用，可以对测试用例进行修改，比如加标签、删除测试用例、对测试用例排序 """

    # 示例1：删除指定名称的测试用例
    # items = [item for item in items if "TEST_导航" not in item.name]
    # 示例2：删除指定标签的测试用例
    # items = [item for item in items if "notfind" not in item.keywords]
    # 示例3：按照名称排序
    # items = sorted(items, key=lambda item: item.name)


def pytest_runtest_setup(item: Item):
    """ 每个测试用例执行前被调用，可以增加判断，排除某些测试用例 """

    # 示例1：跳过指定名称的测试用例
    # if "TEST_导航" in item.name:
    #     pytest.skip("指定的测试用例")
    # 示例2：跳过指定标签的测试用例
    # if "notfind" in item.keywords:
    #     pytest.skip("指定的测试用例")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """ 每个测试用例的setup call teardown时被调用，测试结果在 call 阶段被记录 """

    out = yield
    report = out.get_result()
    if report.when == "call":
        # 通过report.outcome来获取测试结果 [failed passed skipped]

        # 测试用例失败时，终止测试进程
        # if report.outcome == "failed":
        #     pytest.exit(ExitCode.TESTS_FAILED)

        return
    if report.when == "teardown":
        report.description = str(item.function.__doc__)


# 修改测试报告(添加标题)
def pytest_html_report_title(report):
    report.title = title


# 修改测试报告(添加测试者)
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p(f"Tester: {tester}")])


# 修改测试报告的表格头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(3, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


# 修改测试报告的表格内容
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(3, html.td(datetime.datetime.utcnow(), class_='col-time'))
    cells.pop()


########################################################################################################################
#                                                                                                                      #
#                                                     下面是固件                                                         #
#                                                                                                                      #
########################################################################################################################


@pytest.fixture(scope='session', autouse=True)
def rbk():
    rbk = rbklib("58.34.177.163", push_flag=True)
    d = rbk.robot_push_config_req(included_fields=["x", "y", "angle", "task_status", "current_station", "errors"])
    if d.get("ret_code") != 0:
        raise Exception("配置推送失败")
    # 抢占控制权
    rbk.robot_config_lock_req("Test")
    yield rbk
    # 释放控制权
    rbk.robot_config_unlock_req()
