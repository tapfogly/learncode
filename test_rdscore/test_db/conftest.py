from dataclasses import replace
from pathlib import Path
from shutil import copy
import pytest
import sys
sys.path.append("../..")
from APILib.orderLib import *


@pytest.fixture(scope="module", autouse=True)
def core()->OrderLib:
    c = OrderLib(getServerAddr())
    c.modifyParam({"RDSDispatcher": {"ClearDBOnStart": False}})
    return c


def win_kill_proc_by_port(port):
    cmd = 'for /f "tokens=5" %a in (\'netstat -ano ^| find "0.0.0.0:' + str(
        port)+'" ^| find "LISTENING"\') do taskkill /f /pid %a'
    print(cmd)
    os.system(cmd)


def kill_core():
    win_kill_proc_by_port(8088)


def remove_sqlite_files_by_prefix(prefix, path):
    '''删除sqlite文件'''
    for p in path.glob('*'):
        print(p.name)
        if p.name.startswith(prefix):
            if p.is_file():
                p.unlink()
                print("deleted: "+p.name)


def start_core(core_exe_dir):
    '''启动RDSCore'''
    # subprocess.run("rbk.exe", shell=True, cwd=core_exe_dir, capture_output=False)
    # 闪退
    # os.chdir(core_exe_dir)
    # os.system('chdir  && start rbk.exe /K')

    # 没有分离输出
    # openRDSCore(getExeDir())
    subprocess.call("start /wait rbk.exe", shell=True,
                    cwd=core_exe_dir, creationflags=subprocess.DETACHED_PROCESS)


# @pytest.fixture
def replace_db(src_dir):
    '''上传数据库文件'''
    db_dir = Path(getDataDir(), "db")
    print("db dir: " + str(db_dir.absolute()))
    kill_core()
    time.sleep(15)
    remove_sqlite_files_by_prefix("orders", db_dir)
    # copy
    path = Path(src_dir)
    for p in path.glob("*"):
        if p.name.startswith("orders"):
            print(f"Copying: {p.absolute()}\nto: {Path(db_dir, p.name)}")
            copy(p.absolute(), Path(db_dir, p.name))

    runRDSCore(getExeDir())
    time.sleep(3)


@pytest.fixture
def db_select():
    '''换成用于select的数据库'''
    replace_db("dbs/select/")

# @pytest.fixture
# def db_large_select():
#     replace_db("db/large-select/")

if __name__ == '__main__':
    replace_db("dbs/select/")

    print("Done")
