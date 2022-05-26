import sys
sys.path.append("..")
from APILib.rbklib import *
import json

def pytest_configure(config):
    r = rbklib(ip = getIP())
    data = r.getStatusInfo()
    print(json.dumps(data, indent=1))
    if config is not None:
        medata = config._metadata
        config._metadata = dict()
        config._metadata["version"] = data.get("version", "None")
        config._metadata["product"] = "Robokit"
        config._metadata["Python"] = medata.get("Python")
        config._metadata["Platform"] = medata.get("Platform")
if __name__ == "__main__":
    pytest_configure(None)