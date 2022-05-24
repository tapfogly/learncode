import sys
sys.path.append("..")
from APILib.orderLib import *
import json

def pytest_configure(config):
    order = OrderLib(getServerAddr())
    r = order.getPing()
    medata = config._metadata
    config._metadata = dict()
    config._metadata["version"] = r.get("version", "None")
    config._metadata["product"] = r.get("product", "None")
    config._metadata["Python"] = medata.get("Python")
    config._metadata["Platform"] = medata.get("Platform")