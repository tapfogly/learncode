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


    """
    OrderLibCom 是封装好的 RDSCode 通用接口类
    """

class OrderLibCom:
    def __init__(self, ip: str):
        self.ip = ip
        self.port = 8088
        self.url = "http://" + self.ip + ":" + str(self.port)
        self.path = ""
        self.header = {"Content-Type": "application/json"}

    def data_buffer(self, method: str = "post", params=None, **kwargs):
        if kwargs.get("array"):
            kwargs = kwargs["array"]

        comple_url = self.url + self.path
        
        print("*******【" + method + " " + comple_url + " 】*******")
        
        option = getattr(requests, method, None)
        if not method:
            return
        res = option(comple_url, params=params, json=kwargs, headers=self.header)
        
        print("*" * 20 + "【    响应信息   】" + "*" * 20)
        print("*" * 20 + "【Http 状态码：" + str(res.status_code) + "】" + "*" * 20)

        try:
            print(json.dumps(res.json(), indent=4, separators=(",", ":")))
        except:
            pass
        
        return res

    def set_simple_order(self, **kwargs):
        '''
        创建普通运单
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ezno0d
        请求数据说明：
            id (string): 运单 ID，需保证宇宙唯一，可以是任意值，对长度没有限制，不可缺省。
            blocks (object array): 运单的动作块，一个运单是又多个动作块组成；动作块可以看出是单一的动作，不可缺省。
            complete (bool): 运单是否封口， True 代表封口，后续不可再添加额外动作块，False 则反之。 不可缺省。
            externalId (string): 外部单号，可以不唯一；用户可以通过外部单号查询运单详情。
            vehicle (string): 指定机器人，要求系统就当前运单指定给特定机器人；
                              若不填，则系统会根据当前运行情况自动选择合适的机器人派单
            group (string): 指定机器人组，要求系统就当前运单指定给特定机器人组；
                            若不填，调度系统会从当前所有机器人中选择能够去终点的机器人。
            label (string): 指定机器人标签，要求系统就当前运单指定给特定标签的机器人。
            keyRoute (string array): 关键点，用于辅助确定派单机器人；若不填，则系统会根据当前运行情况自动选择合适的机器人派单。
                                     建议填写。关键点不能是 SELF_POSITION。
            keyTask (string): 为 "load"或者"unload"，如果填写其他字段会被自动忽略，用于辅助确定派单机器人；
                              若不填，则系统会根据当前运行情况自动选择合适的机器人派单。
            priority (string): 运单优先级，数字越大代表订单优先级越高；可不填。

        动作块请求数据说明：
            blockId (string): 动作块 ID，需保证宇宙唯一，可以是任意值，对长度没有限制，不可缺省。
            location (string): 目的地名称，站点名，例如：AP28。如果为 SELF_POSITION 表示该动作为原地动作，不可缺省。
            operation (string): 执行机构动作,动作相关的 operation 可参考固定路径导航并执行动作。 如：JackLoad, Script
            postAction (object): 此字段为 block 完成状态回调。
            执行脚本：
                scriptName/script_name (string): 机器人中的脚本名称。
                scriptArgs/script_args (object): 脚本中定义的参数。
            机构动作：
                operationArgs/operation_args (object)：动作参数。
            库位动作：
                binTask (string): 库位中配置的库位动作的 key。
                goodsId (string): 货物编号，上位系统可以通过此参数管理货物状态。可不填，如不填，系统会自动生成随机编号
        '''
        self.path = "/setOrder"
        return self.data_buffer(**kwargs)

    def set_merged_order(self, **kwargs):
        '''
        创建拼合运单
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/bn0q09
        请求数据说明：
            id (string): 任务 ID，需要宇宙唯一，不可缺省。
            fromLoc (string): 取货库位名称，不可缺省。
            toLoc (string): 放货库位名称，不可缺省。
            vehicle (string): 指定机器人，要求系统就当前运单指定给特定机器人；
                              若不填，则系统会根据当前运行情况自动选择合适的机器人派单。
            group (string): 指定机器人组，要求系统就当前运单指定给特定机器人组；
                            若不填，则系统会根据当前运行情况自动选择合适的机器人派单。
            goodsid (string): 货物编号，上位系统可以通过此参数管理货物状态。可不填，如不填，系统会自动生成随机编号。
            loadPostAction (object): 取货后回调，可用来通知上位系统取货完成。
            unloadPostAction (object): 放货后回调，可用来通知上位系统取货完成。
        '''
        self.path = "/setOrder"
        return self.data_buffer(**kwargs)

    def mark_complete(self, id):
        '''
        运单封口，封口后无法继续添加动作块
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/xv9w7a
        请求数据说明：
            id (string): 需要封口的运单 ID，不可缺省。
            idList (string): 需要封口的运单 ID 列表，不可缺省。
        '''
        self.path = "/markComplete"
        return self.data_buffer(**id)

    def terminate(self, **kwargs):
        '''
        终止订单
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/agqtg8
        终止单个运单：
            id (string): 运单 ID, 不可缺省。
            disableVehicle (bool): 指示执行此运单的机器人后续是否接单的标识，true=执行此运单的机器人在此运单终止后不再接单，
                                   false=此运单终止后依然可以继续接单。可不填，默认为 true。
        终止多个运单：
            idList (string array): 运单 ID, 为空字符串数组时,终止所有运单。不可缺省。
            disableVehicle (bool): 指示执行此运单的机器人后续是否接单的标识，true=执行此运单的机器人在此运单终止后不再接单，
                                   false=此运单终止后依然可以继续接单。可不填，默认为 true。
        终止指定机器人运单：
            vehicles (string array): 机器人名列表。
            disableVehicle (bool): 指示执行此运单的机器人后续是否接单的标识，true=执行此运单的机器人在此运单终止后不再接单，
                                   false=此运单终止后依然可以继续接单。可不填，默认为 true.
            clearAll (bool): 是否清除此机器人所接的所有运单，所有运单指的是正在执行的当前运单和已经分配给该车还未执行的运单。
                             可不填，默认为false，即只终止当前运单
        '''
        self.path = "/terminate"
        return self.data_buffer(**kwargs)

    def order_details(self, id: str):
        '''
        通过运单号查询运单状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gu1tzm
        '''
        self.path = "/orderDetails" + '/' + id
        return self.data_buffer("get")

    def order_externalid(self, externalId: str):
        '''
        通过外部单号查询运单状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ig7mmi
        '''
        self.path = "/orderDetailsByExternalId" + "/" + externalId
        return self.data_buffer("get")

    def order_by_block_id(self, blockId: str):
        '''
        通过动作块 ID 查询运单状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ehbqta
        '''
        self.path = "/orderDetailsByBlockId" + "/" + blockId
        return self.data_buffer("get")

    def order(self, page_num: int = None, order_size: int = None, order_by: str = None
              , order_method: str = None, where: dict = None):
        '''
        通过参数分页查询系统内的运单集合
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/co5ea9
        请求参数：
            page (number): 页码数，如果不传默认为1
            size (number): 每页运单数量，如果不传默认为20
            orderBy (string): 排序的字段，可以为 createTime，terminalTime 和 priority，默认为 createTime
            orderMethod (string): 排序方法，可以为 descending 和 ascending，默认为 descending 降序
            where (object string): 过滤条件，为 JSON 字符串，不传时不做过滤

        过滤条件：
            {
                "relation":"AND",   表示多个查询条件的组合方式，支持AND, OR
                "predicates":[      每列的条件,格式为 [列名，操作符，值]，三个字符串，支持的操作有：GT, LT, EQ, LIKE, NE, IN
                    ["createTime", "GT", "1642846097186"],  创建时间大于指定值
                    ["createTime", "LT", "1642846097200"],  创建时间小于指定值
                    ["vehicle", "EQ", "AMB-01"],   执行机器人为 AMB-01
                    ["state", "EQ", "FINISHED"]    状态为 FINISHED
                ]
            }
        '''
        self.path = "/orders"
        params = {}
        if page_num:
            params["page"] = page_num
        if order_size:
            params["size"] = order_size
        if order_by:
            params["orderBy"] = order_by
        if order_method:
            params["orderMethod"] = order_method
        if where:
            params["where"] = json.dumps(where)

        return self.data_buffer("get", params=params)

    def set_priority(self, order_id: str, priority: int):
        '''
        修改运单优先级
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ga4vv9
        '''
        d = {"id": order_id, "priority": priority}
        self.path = "/setPriority"
        return self.data_buffer(**d)

    def set_label(self, order_id: str, label: str):
        '''
        修改运单 label
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/hmg7en
        '''
        d = {
            "id": order_id,
            "label": label
        }
        self.path = "/setLabel"
        return self.data_buffer(**d)

    def clear_cache(self, order_type: str, timestamp: int):
        '''
        清除运单缓存
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/lga0y8
        请求数据：
            type (string): 需要清除的缓存类型，目前可为普通运单=“orders”和拼合单=“simpleOrders”。
            timestamp (int): 格式为 Unix timestamp，单位为秒（s），代表需要清除指定时间戳之前且状态为终态的运单。
        时间戳转换工具 https://www.unixtimestamp.com/
        '''
        d = {
            "type": order_type,
            "timestamp": timestamp
        }
        self.path = "/clearCache"
        return self.data_buffer(**d)

    def block(self, page_num: int = None, order_size: int = None, order_by: str = None
              , order_method: str = None, where: dict = None):
        '''
        分页查询动作块信息
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/xeab6m
        请求参数：
            page (number): 页码数，如果不传默认为1
            size (number): 每页运单数量，如果不传默认为20
            orderBy (string): 排序的字段，可以为 createTime，terminalTime 和 priority，默认为 createTime
            orderMethod (string): 排序方法，可以为 descending 和 ascending，默认为 descending 降序
            where (object string): 过滤条件，为 JSON 字符串，不传时不做过滤

        过滤条件：
            {
                "relation":"AND",   表示多个查询条件的组合方式，支持AND, OR
                "predicates":[      每列的条件,格式为 [列名，操作符，值]，三个字符串，支持的操作有：GT, LT, EQ, LIKE, NE, IN
                    ["createTime", "GT", "1642846097186"],  创建时间大于指定值
                    ["createTime", "LT", "1642846097200"],  创建时间小于指定值
                    ["vehicle", "EQ", "AMB-01"],   执行机器人为 AMB-01
                    ["state", "EQ", "FINISHED"]    状态为 FINISHED
                ]
            }
        '''
        self.path = "/blocks"
        params = {}
        if page_num:
            params["page"] = page_num
        if order_size:
            params["size"] = order_size
        if order_by:
            params["orderBy"] = order_by
        if order_method:
            params["orderMethod"] = order_method
        if where:
            params["where"] = json.dumps(where)

        return self.data_buffer("get", params=params)

    def add_block(self, **kwargs):
        '''
        追加运单的动作块
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/feswvi
        '''
        self.path = "/addBlocks"
        return self.data_buffer(**kwargs)

    def re_do_failed_order(self, car_name: dict):
        '''
        重做失败运单
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/nsz0pc
        '''
        self.path = "/redoFailedOrder"
        return self.data_buffer(**car_name)

    def manual_finished(self, car_name: dict):
        '''
        手动完成动作块
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/kvx3p9
        '''
        self.path = "/manualFinished"
        return self.data_buffer(**car_name)

    def block_details_by_id(self, block_id: str = None):
        '''
        通过动作块 id 查询动作块状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/zg0w7z
        '''
        self.path = "/blockDetailsById"
        if block_id:
            self.path = self.path + "/" + block_id
        return self.data_buffer("get")

    def robot_status(self, devices: str = None, paths: str = None):
        '''
        获取所有机器人信息
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/pr67d7
        '''
        self.path = "/robotsStatus"
        d = {}
        if devices:
            d["devices"] = devices
        if paths:
            d["paths"] = paths
        return self.data_buffer("get", params=d)

    def robot_smap(self, robot_name: str, map: str):
        '''
        获取指定机器人的地图
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/fg17p8
        '''
        self.path = "/robotSmap"
        d = {"vehicle": robot_name, "map": map}
        return self.data_buffer(**d)

    def lock(self, robot_name: dict):
        '''
        获取机器人的控制权
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/yl3iul
        '''
        self.path = "/lock"
        return self.data_buffer(**robot_name)

    def unlock(self, robot_name: dict):
        '''
        释放机器人控制权
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/kv06kf
        '''
        self.path = "/unlock"
        return self.data_buffer(**robot_name)

    def set_params(self, data: dict):
        '''
        临时修改机器人的参数
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/tiv64r
        '''
        self.path = "/setParams"
        return self.data_buffer(**data)

    def save_params(self, data: dict):
        '''
        永久修改机器人的参数
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gdd5e9
        '''
        self.path = "/saveParams"
        return self.data_buffer(**data)

    def reload_params(self, data: dict):
        '''
        永久修改机器人的参数
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gdd5e9
        '''
        self.path = "/reloadParams"
        return self.data_buffer(**data)

    def switch_map(self, data: dict):
        '''
        切换机器人当前使用的地图
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/vpusko
        '''
        self.path = "/switchMap"
        return self.data_buffer(**data)

    def dispatchable(self, data: dict):
        '''
        更改机器人的接单状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ofmfrc
        '''
        self.path = "/dispatchable"
        return self.data_buffer(**data)

    def reloc_confirm(self, data: dict):
        '''
        确认机器人的定位状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/dbgzwq
        '''
        self.path = "/reLocConfirm"
        return self.data_buffer(**data)

    def goto_site_pause(self, data: dict):
        '''
        暂停机器人导航
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/yr8wa8
        '''
        self.path = "/gotoSitePause"
        return self.data_buffer(**data)

    def goto_site_resume(self, data: dict):
        '''
        继续机器人导航
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/btphx9
        '''
        self.path = "/gotoSiteResume"
        return self.data_buffer(**data)

    def get_status(self):
        '''
        获取仿真机器人可修改状态列表
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gioyes
        '''
        self.path = "/getSimRobotStateTemplate"
        return self.data_buffer("get")

    def update_state(self, data: dict):
        '''
        更新仿真机器人状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/qy8pg3
        '''
        self.path = "/updateSimRobotState"
        return self.data_buffer(**data)

    def set_container_goods(self, data: dict):
        '''
        绑定货物到指定料箱
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ediyzc
        '''
        self.path = "/setContainerGoods"
        return self.data_buffer(**data)

    def clear_goods(self, data: dict):
        '''
        解绑指定货物
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/mc16ub
        '''
        self.path = "/clearGoods"
        return self.data_buffer(**data)

    def clear_container(self, data: dict):
        '''
        从指定料箱解绑货物
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/qai7hk
        '''
        self.path = "/clearContainer"
        return self.data_buffer(**data)

    def clear_all_container(self, data: dict):
        '''
        从所有料箱解绑货物
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/tqy5gr
        '''
        self.path = "/clearAllContainersGoods"
        return self.data_buffer(**data)

    def get_block_group(self, data: dict):
        '''
        占用互斥组
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/bwvr6h
        '''
        self.path = "/getBlockGroup"
        return self.data_buffer(**data)

    def release_block_group(self, data: dict):
        '''
        释放互斥组
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/usftie
        '''
        self.path = "/releaseBlockGroup"
        return self.data_buffer(**data)

    def block_status(self, data: dict):
        '''
        查询互斥组状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/iogplz
        '''
        self.path = "/blockGroupStatus"
        return self.data_buffer(**data)

    def call_terminal(self, data: dict):
        '''
        与终端交互
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/wbno17
        '''
        self.path = "/callTerminal"
        return self.data_buffer(**data)

    def devices_details(self, devices: str = None):
        '''
        查询设备状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ciqdop
        '''
        self.path = "/devicesDetails"
        return self.data_buffer("get", params=devices)

    def bin_details(self, group: dict = None, bin_id: str = None):
        '''
        查询库位状态
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gi5nlg
        '''
        self.path = "/binDetails"
        params = None
        if group:
            params = group
        elif bin_id:
            params = id
        return self.data_buffer("get", params=params)

    def bin_check(self, bins: dict):
        '''
        检查库位有效性
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/rnyg31
        '''
        self.path = "/binCheck"
        return self.data_buffer(**bins)

    def call_door(self, doors: list):
        '''
        与自动门交互
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ivhor5
        '''
        self.path = "/callDoor"
        return self.data_buffer(array=doors)

    def disable_door(self, doors: dict):
        '''
        禁用自动门
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gllodv
        '''
        self.path = "/disableDoor"
        return self.data_buffer(**doors)

    def call_lift(self, lifts: list):
        '''
        与提升机交互
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ghcc93
        '''
        self.path = "/callLift"
        return self.data_buffer(array=lifts)

    def disable_lift(self, lifts: dict):
        '''
        禁用提升机
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/smnfnf
        '''
        self.path = "/disableLift"
        return self.data_buffer(**lifts)

    def get_disable_points(self):
        '''
        查询禁用的点位
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/dm1ozg
        '''
        self.path = "/getDisablePoints"
        return self.data_buffer("get")

    def disable_points(self, path_id: dict):
        '''
        禁用点位
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/xw4x7h
        '''
        self.path = "/disablePoint"
        return self.data_buffer(**path_id)

    def enable_points(self, path_id: dict):
        '''
        启用点位
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/xs5h9h
        '''
        self.path = "/enablePoint"
        return self.data_buffer(**path_id)

    def get_disable_path(self):
        '''
        查询禁用的线路
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/qexb1g
        '''
        self.path = "/getDisablePaths"
        return self.data_buffer("get")

    def get_enable_path(self, path: dict):
        '''
        启用线路
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/gil63l
        '''
        self.path = "/enablePath"
        return self.data_buffer(**path)

    def disable_path(self, path_id: dict):
        '''
        禁用线路
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/mttt8m
        '''
        self.path = "/disablePath"
        return self.data_buffer(**path_id)

    '''
    内部使用的接口
    '''

    def download_scene(self):
        '''
        下载场景
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/kl0mtx
        '''
        self.path = "/downloadScene"
        return self.data_buffer("get")

    def download_scene_file(self, path: dict):
        '''
        下载场景资源包中指定的文件
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/vsaqst
        '''
        self.path = "/downloadSceneFiles"
        return self.data_buffer(**path)

    def upload_scene(self):
        '''
        上传场景
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/yxxv2s
        '''
        self.path = "/uploadScene"
        return self.data_buffer()

    def sync_scene(self):
        '''
        还原场景
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/ebwgsw
        '''
        self.path = "/syncScene"
        return self.data_buffer()

    def get_scene(self):
        '''
        获取场景信息
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/yi3qup
        '''
        self.path = "/scene"
        return self.data_buffer("get")

    def get_profiles(self, file_name: dict):
        '''
        获取配置文件
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/rzsnvx
        '''
        self.path = "/getProfiles"
        return self.data_buffer(**file_name)

    def ping(self):
        '''
        连通性测试
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/mmgk33
        '''
        self.path = "/ping"
        return self.data_buffer("get")

    def license(self):
        '''
        获取license信息
        接口详情 https://seer-group.yuque.com/pf4yvd/lg4q1h/yog6ww
        '''
        self.path = "/licInfo"
        return self.data_buffer("get")






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


