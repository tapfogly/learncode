import sys
sys.path.append("../..")

from APILib.orderLib import *
from pathlib import Path


def test_read_containers_from_model(core:OrderLib):
    core.uploadScene(Path(Path(__file__).parents[0],"scene_container.zip"))
    time.sleep(10)
    status = core.robotStatus("RD-TEST-2")
    assert len(status['rbk_report']['containers']) == 7
    core.uploadScene(Path(Path(__file__).parents[0], "scene.zip"))
    time.sleep(5)

if __name__ == '__main__':
    print(Path(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))