# robokit#1067
from pymodbus.client.sync import ModbusTcpClient
import pytest
import sys
sys.path.append('../..')
from APILib.orderLib import *
import logging

FORMAT = (
    "%(asctime)-15s %(threadName)-15s "
    "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

core = OrderLib(getServerAddr())
def setup_module():
    """执行这个脚本的用例前需要的准备内容
    """
    global core
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, "rds_20220602172845.zip")
    core.uploadScene(p)
    time.sleep(5)

def test_read_block_group_status():
    '''
    测试modbus读到的占用状态是否合法
    '''
    client = ModbusTcpClient('127.0.0.1', 502)
    conn = client.connect()
    assert conn
    result = client.read_holding_registers(0, 10, unit=1)
    assert result.registers == [0]*10
    client.close()


def test_acquire_block_group():
    '''
    测试通过modbusTCP协议申请互斥区
    '''
    client = ModbusTcpClient('127.0.0.1', 502,timeout=10)
    conn = client.connect()
    assert conn
    result = client.write_registers(13, [1], unit=1)
    assert not result.isError()
    time.sleep(1)
    result = client.read_holding_registers(12, 6, unit=1)
    assert result.registers == [1]*6
    client.write_registers(12,[0]*4, unit=1)
    assert not result.isError()
    time.sleep(1)
    result = client.read_holding_registers(12,6, unit=1)
    assert result.registers == [0] * 6
    client.close()


if __name__ == '__main__':
    # test_acquire_block_group()
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
