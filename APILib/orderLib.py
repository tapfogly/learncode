import json
import requests
import uuid
import os
import time
import subprocess
import multiprocessing
import rbklib
from typing import List

def getConfigValue(key:str)->str:
    p = os.path.dirname(__file__)
    p = os.path.dirname(p)
    config_path = os.path.join(p, "config.json")
    with open(config_path, "r") as f:
        j = json.load(f)
        return j.get(key,"")


def getServerAddr()->str:
    """获取服务器的地址
    Returns:
        str: 服务器地址
    """
    return getConfigValue("rdscore_addr")

def getDataDir()->str:
    '''获取数据目录的绝对路径
    Returns:
        str: 数据目录路径
    '''
    return getConfigValue("rdscore_data_dir")
    # todo 验证是否存在文件夹

def getExeDir()->str:
    '''获取rbk.exe所在目录的绝对路径
    Returns:
        str: rbk.exe目录路径
    '''
    return getConfigValue("rdscore_exe_dir")

_orderLif_headers = {'Content-Type': 'application/json'}

def getUUID():
    order_id = uuid.uuid4()
    order_id = str(order_id)
    order_id = ''.join(order_id.split('-'))
    return order_id

def getLogAfterT(fdir = None, t0 = None):
    if t0 is None or fdir is None:
        return None
    list_dir = os.listdir(fdir)
    log_dict = dict()
    for d in list_dir:
        if not os.path.isdir(d):
            tail = os.path.splitext(d)
            if tail[-1] == ".log":
                full_path = os.path.join(fdir, d)
                log_dict[os.path.getctime(full_path)] = d
    log_dict = sorted(log_dict.items(), key= lambda s :s[0], reverse=True)
    out_log = []
    for l in log_dict:
        if l[0] > t0:
            out_log.append(os.path.join(fdir, l[1]))
    return out_log

def openRDSCore(rdsDir = None):
    subprocess.call("rbk.exe", cwd = rdsDir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

def runRDSCore(rdsDir = None):
    p1 = multiprocessing.Process(target = openRDSCore, args=(rdsDir,))
    p1.daemon = True
    p1.start()
    return p1

def getLeasetLog(fdir = None):
    if fdir is None:
        return None
    list_dir = os.listdir(fdir)
    log_dict = dict()
    for d in list_dir:
        if not os.path.isdir(d):
            tail = os.path.splitext(d)
            if tail[-1] == ".log":
                full_path = os.path.join(fdir, d)
                log_dict[os.path.getctime(full_path)] = d
    log_dict = sorted(log_dict.items(), key= lambda s :s[0], reverse=True)
    tf = os.path.join(fdir, log_dict[0][1])
    print(tf)
    return tf


class OrderLib:
    def __init__(self, ip) -> None:
        self.ip = ip
        self.tcp_ip = self.ip.split("/")[-1]
        self.tcp_ip = self.tcp_ip.split(":")[0]
        self.rbk = rbklib.rbklib(self.tcp_ip, True)

    def __del__(self):
        self.rbk.__del__()
        
    def selectOrder(self, order_id):
        r = requests.get(self.ip + "/orderDetails/{}".format(order_id), headers=_orderLif_headers)
        return r.json()

    def gotoOrder(self, vehicle = None, location = None, group = None, complete = True,
    binTask = None, operation = None, operationArgs = None,
    scriptName = None, scriptArgs = None, goodsId = None,
    keyRoute = None,
    sleepTime = None,
    priority = None,
    keyTask = None,
    label = None):
        uuid = getUUID()
        if type(vehicle) is str:
            uuid = vehicle+":"+ uuid
        if location != None:
            datas = json.dumps(
            {
                "blocks": [
                    {
                        "blockId": uuid+":0",
                        "location": location,
                        "binTask": ("" if type(binTask) is not str else binTask),
                        "operation": ("" if type(operation) is not str else operation),
                        "operationArgs":("" if type(operationArgs) is not dict else operationArgs),
                        "scriptName":("" if type(scriptName) is not str else scriptName),
                        "scriptArgs":("" if type(scriptArgs) is not dict else scriptArgs),
                        "goodsId":("" if type(goodsId) is not str else goodsId)
                    }
                ],
                "priority":(0 if type(priority) is not int else priority),
                "complete": complete,
                "id": uuid,
                "vehicle": ("" if type(vehicle) is not str else vehicle),
                "group": ("" if type(group) is not str else group),
                "label": ("" if type(label) is not str else label),
                "keyRoute" :(keyRoute if isinstance(keyRoute,str) or isinstance(keyRoute, list) else ""),
                "keyTask":("" if type(keyTask) is not str else keyTask)
            }
            )
        else:
            datas = json.dumps(
            {
                "blocks": [],
                "complete": complete,
                "id": uuid,
                "vehicle": ("" if type(vehicle) is not str else vehicle),
                "group": ("" if type(group) is not str else group),
                "keyRoute" :([] if type(keyRoute) is not list else keyRoute),
                "keyTask":("" if type(keyTask) is not str else keyTask),
                "label": ("" if type(label) is not str else label)
            }
            )            
        print(datas)
        r = requests.post(self.ip + "/setOrder", data=datas, headers=_orderLif_headers)
        if sleepTime is not None:
            time.sleep(sleepTime)
        return uuid

    def simpleOrder(self, fromLoc, toLoc, goodsdId = None, vehicle = None):
        uuid = getUUID()
        datas = json.dumps(
        {
            "fromLoc": fromLoc,
            "toLoc":toLoc,
            "id": uuid,
            "goodsId":("" if type(goodsdId) is not str else goodsdId),
            "vehicle": ("" if type(vehicle) is not str else vehicle)
        }
        )
        print(datas)
        r = requests.post(self.ip + "/setOrder", data=datas, headers=_orderLif_headers)
        return uuid    

    def addBlock(self, orderId = None, location = None, 
    binTask = None, operation = None, operationArgs = None,
    scriptName = None, scriptArgs = None, goodsId = None,
    sleepTime = None):
        uuid = orderId + ":" + getUUID()
        datas = json.dumps(
        {
            "blocks": [
                {
                    "blockId": uuid+":0",
                    "location": location,
                    "binTask": ("" if type(binTask) is not str else binTask),
                    "operation": ("" if type(operation) is not str else operation),
                    "operationArgs":("" if type(operationArgs) is not dict else operationArgs),
                    "scriptName":("" if type(scriptName) is not str else scriptName),
                    "scriptArgs":("" if type(scriptArgs) is not dict else scriptArgs),
                    "goodsId":("" if type(goodsId) is not str else goodsId)
                }
            ],
            "id": orderId,
        }
        )
        print(datas)
        r = requests.post(self.ip + "/addBlocks", data=datas, headers=_orderLif_headers)
        if sleepTime is not None:
            time.sleep(sleepTime)
        return uuid    

    def manualFinishedCurrentBlock(self, name):
        datas = json.dumps(
        {
            "vehicles":[name]
        }
        )
        print("manualFinished: ", datas)
        r = requests.post(self.ip+"/manualFinished", data=datas, headers=_orderLif_headers)
        return r

    def markComplete(self, orderId:str):
        datas = json.dumps(
        {
            "id":orderId
        }
        )
        print("markComplete: ", datas)
        r = requests.post(self.ip+"/markComplete", data=datas, headers=_orderLif_headers)
        return r

    def terminateCurrentTask(self, vehicles, disableVehicle):
        datas = json.dumps(
        {
            "vehicles":[vehicles],
            "disableVehicle": disableVehicle
        }
        )
        r = requests.post(self.ip+"/terminate", data=datas, headers=_orderLif_headers)
        return r

    def orderDetails(self, orderId):
        r = requests.get(self.ip+"/orderDetails/"+orderId)
        out = dict()
        try:
            out = json.loads(r.text)
        except:
            pass
        return out

    def setOrderLabel(self, orderId, label):
        r = requests.post(self.ip+"/setLabel",data=json.dumps({"id":orderId,"label":label}), headers = _orderLif_headers )
        return r

    def setOrderPriority(self, orderId, priority):
        r = requests.post(self.ip + '/setPriority', data = json.dumps({"id":orderId, "priority":priority}), headers = _orderLif_headers)
        return r

    def terminateAll(self,vehicle):
        if isinstance(vehicle, str):
            datas = json.dumps(
            {
                "vehicles":[vehicle],
                "clearAll":True
            }
            )
            r = requests.post(self.ip+"/terminate", data=datas, headers=_orderLif_headers)
            return datas
        if isinstance(vehicle, list):
            datas = json.dumps(
            {
                "vehicles":vehicle,
                "clearAll":True
            }
            )
            r = requests.post(self.ip+"/terminate", data=datas, headers=_orderLif_headers)
            return datas
        return "wrong vehicle {}".format(vehicle)

    def terminateIdList(self, ids):
        datas = json.dumps(
        {
            "idList":ids,
        }
        )
        r = requests.post(self.ip+"/terminate", data=datas, headers=_orderLif_headers)
        return datas        

    def terminateId(self, order_id, disableVehicle = None):
        if isinstance(disableVehicle, bool):
            datas = json.dumps(
            {
                "id":order_id,
                "disableVehicle": disableVehicle
            }
            )
        else:
            datas = json.dumps(
            {
                "id":order_id
            }
            )            
        r = requests.post(self.ip+"/terminate", data=datas, headers=_orderLif_headers)
        return datas               
        
    def dispatchable_org(self, name, type_str, finished:bool = False):
        if type(name) is not list:
            name = [name]
        if name == "dispatchable":
            datas = json.dumps(
            {
                "vehicles":name,
                "type":type_str
            }
            )
        else:
            datas = json.dumps(
            {
                "vehicles":name,
                "type":type_str,
                "finishedCurrentOrders": finished
            }
            )
        print(datas)
        r = requests.post(self.ip + "/dispatchable", data=datas, headers=_orderLif_headers)
        return r    

    def undispatchable_unignore(self, name, finished = False):
        return self.dispatchable_org(name, "undispatchable_unignore", finished)

    def undispatchable_ignore(self, name, finished = False):
        return self.dispatchable_org(name, "undispatchable_ignore", finished)

    def dispatchable(self, name):
        return self.dispatchable_org(name, "dispatchable")

    def locked(self, name=None):
        if name is None:
            datas = json.dumps(
            {
            "vehicles": []
            }
            )
        else:
            if type(name) is not list:
                name = [name]
            datas = json.dumps(
            {
            "vehicles": name
            }
            )
        r = requests.post(self.ip+"/lock", data=datas, headers=_orderLif_headers)
        return r

    def gotoSiteCancel(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps(
        {
        "vehicles": name
        }
        )
        r = requests.post(self.ip+"/gotoSiteCancel", data=datas, headers=_orderLif_headers)
        return r
    def gotoSitePause(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps({"vehicles":name})
        r =requests.post(self.ip + '/gotoSitePause',data=datas,headers=_orderLif_headers)
        return r
    def gotoSiteResume(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps({"vehicles":name})
        r = requests.post(self.ip+'/gotoSiteResume', data=datas, headers = _orderLif_headers)
        return r
    def uploadScene(self, name:str=""):
        p = os.path.dirname(__file__)
        p = os.path.dirname(p)
        scene_path = os.path.join(p,name)
        with open(scene_path, 'rb') as f:
            datas = f.read()        
            r = requests.post(self.ip+"/uploadScene", data= datas)
            print(r.status_code)
        return r

    def waitForOrderFinish(self, uuid):
        status = "RUNNING"
        while status != "FINISHED" and status != "STOPPED":
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("waitForOrderFinish", uuid, out , status)
            time.sleep(1)    

    def waitForOrderFinishTimeout(self, uuid, timeout=30):
        status = "RUNNING"
        time_elapsed = 0
        while status != "FINISHED" and status != "STOPPED" :
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("waitForOrderFinish", uuid, out , status)
            time.sleep(1)    
            time_elapsed+=1
            print(time_elapsed)
            if time_elapsed > timeout:
                print("waitForOrderFinish", uuid, out, status, "TIMEOUT")
                return
    def isOrderFinished(self, uuid, timeout=30):
        status = "RUNNING"
        time_elapsed = 0
        while status != "FINISHED" and status != "STOPPED" :
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("isOrderFinished", uuid, out , status)
            time.sleep(1)    
            time_elapsed+=1
            print(time_elapsed)
            if time_elapsed > timeout:
                print("TIMEOUT")
                return False    
            if status == "FINISHED":
                return True
            if status == "STOPPED":
                return False

    def clearRobotAllError(self, name):
        if type(name) is not list:
            if name == "":
                name = []
            elif type(name) is str:
                name = [name]
        datas = json.dumps(
        {
        "vehicles": name
        }
        )
        r = requests.post(self.ip+"/clearRobotAllError", data=datas, headers=_orderLif_headers)
        return r     

    def getPing(self):
        r = requests.get(self.ip+"/ping")
        return r.json()
    
    def robotsStatus(self):
        r = requests.get(self.ip +"/robotsStatus")
        return r.json()
    
    def getCoreError(self):
        rs = self.robotsStatus()
        return rs['alarms']['errors']
        
    def robotStatus(self, vehicle_id:str):
        data = dict()
        rs = self.robotsStatus()
        for r in rs["report"]:
            if r["vehicle_id"] == vehicle_id:
                data = r
                break
        return data
    def updateSimRobotState(self, datas:dict):
        """设置仿真机器人参数

        Args:
            datas (dict): 这个json见文档 
            https://books.seer-group.com/public/rdscore/master/zh/api/http/robot/updateSimRobotState.html
            https://seer-group.yuque.com/pf4yvd/gp9mgx/xmyicq
        """
        r = requests.post(self.ip+"/updateSimRobotState", data=datas, headers=_orderLif_headers)
        return r

    def modifyParam(self, data:dict()):
        """永久修改参数配置里面的参数

        Args:
            data (dict): 格式如下
            {
                "MoveFactory": {
                    "3DCameraHole": true
                }
            }
        """
        self.rbk.modifyParam(data)
    
    def recoveryParam(self):
        self.rbk.recoveryParam()
    
    def disableDoor(self, names:list, disabled:bool):
        datas = json.dumps(
            {
            "names": names,
            "disabled": disabled
            }
        )
        r = requests.post(self.ip+"/disableDoor", data=datas, headers=_orderLif_headers)
        return r

    def disableLift(self, names:list, disabled:bool):
        datas = json.dumps(
            {
            "names": names,
            "disabled": disabled
            }
        )
        r = requests.post(self.ip+"/disableLift", data=datas, headers=_orderLif_headers)
        return r

    def disablePath(self, name:str):
        datas = json.dumps(
            {
            "id": name
            }
        )
        r = requests.post(self.ip+"/disablePath", data=datas, headers=_orderLif_headers)
        return r        
    def disablePoint(self, name:str):
        datas = json.dumps(
            {
            "id": name
            }
        )
        r = requests.post(self.ip+"/disablePoint", data=datas, headers=_orderLif_headers)
        return r      
    def enablePath(self, name:str):
        datas = json.dumps(
            {
            "id": name
            }
        )
        r = requests.post(self.ip+"/enablePath", data=datas, headers=_orderLif_headers)
        return r      
    def enablePoint(self, name:str):
        datas = json.dumps(
            {
            "id": name
            }
        )
        r = requests.post(self.ip+"/enablePoint", data=datas, headers=_orderLif_headers)
        return r  
    def getDisablePoints(self):
        r = requests.get(self.ip + "/getDisablePoints", headers=_orderLif_headers)
        return r.json()
    def getDisablePaths(self):
        r = requests.get(self.ip + "/getDisablePaths", headers=_orderLif_headers)
        return r.json()
    def pagedQuery(self, path:str, page_num: int = None, page_size: int = None, order_by: str = None, order_method: str = None, relation: str = None, predicates: List[str] = None):
        '''
        page_num: 页数
        page_size: 一页有多少条数据
        order_by: 排序字段
        order_method: 排序方式 descending ascending
        relation: "AND" "OR"
        predicates: [ ["field", "op", "value"], ["state", "EQ", "FINISHED"], ... ]
            op: "GT", "LT", "EQ", "NE", "LIKE", "IN"
        '''
        data = json.dumps(
            {
                "relation": relation,
                "predicates": predicates
            })

        params = {}
        if page_num:
            params['page'] = page_num
        if page_size:
            params['size'] = page_size
        if order_by:
            params['order_by'] = order_by
        if order_method:
            params['order_method'] = order_method
        if relation and predicates:
            params['where'] = data

        r = requests.get(self.ip + "/"+path, params=params,
                         headers=_orderLif_headers)
        return r.json()
if __name__ == "__main__":
    order = OrderLib(getServerAddr())
    order.locked()
    order.gotoOrder(location= "LM314")
    # order.disableDoor(names = ["Door-01"], disabled = False)
    # order.disableLift(names = ["Lift-01"], disabled = False)
    # order.recoveryParam()
    # data = {
    #     "RDSDispatcher":{
    #         "DelayFinishTime":1
    #     }
    # }
    # order.modifyParam(data)
    # order = OrderLib("http://127.0.0.1:8088")
    # order.gotoOrder(binTask="load", location="3-8", vehicle="AMB-05",complete=True, goodsId="hello")
    # order.gotoOrder(binTask="load", location="3-8", vehicle="AMB-05",complete=True, goodsId="world")
    # order.gotoOrder(vehicle="AMB-03",id="LM60")
    # order.clearRobotAllError("AMB-01")
    # uuid1 = order.simpleOrder(fromLoc = "SM05-03", toLoc= "SM06-01",goodsdId=0)
    # print(uuid1)
    # time.sleep(2)
    # uuid2 = order.simpleOrder(fromLoc = "SM05-04", toLoc= "SM06-02",goodsdId=1)
    # print(uuid2)
    # # time.sleep(0.5)
    # # uuid2 = order.simpleOrder(fromLoc = "AP42", toLoc= "AP40")
    # time.sleep(3)
    # print(order.selectOrder(uuid1))
    # print(order.selectOrder(uuid2))
    # print(selectOrder(ip, "e251f18559d14220ae72a130dbd2271a"))
    # # out = orderDetails(ip,"SFL-01:57d5c3b86db54f6daf3d587e7a695840")
    # # print(out)
    # rdsDir = "F:\\SDK\\rbk\\rdscore\\RDSCore-SDK-v0.0.17.0\\RDSCore-SDK-20211118-v0.0.17.0"
    # p1=runRDSCore(rdsDir)
    # curtime = time.time()
    # time.sleep(10)
    # log_dir = "C:\\.SeerRobotics\\rdscore\\diagnosis\\log"
    # print(curtime)
    # print(getLogAfterT(log_dir, curtime))
    # p1.terminate()
    # manualFinishedOrderId(ip, order_id = "123")
    # manualFinishedCurrentTask(ip, name= "agv1")


