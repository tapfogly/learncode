import json
import requests
import uuid
import os
import time
import subprocess
import multiprocessing
import rbklib
from typing import List
from urllib import parse
from datetime import datetime
import calendar
import sqlite3
import json
try:
    import psutil
    library_available = True
except ImportError:
    library_available = False
    print("第三方库未安装，请考虑安装后再试。")

def getConfigValue(key: str) -> str:
    p = os.path.dirname(__file__)
    p = os.path.dirname(p)
    config_path = os.path.join(p, "config.json")
    with open(config_path, "r") as f:
        j = json.load(f)
        return j.get(key, "")


def getServerAddr() -> str:
    """获取服务器的地址
    Returns:
        str: 服务器地址
    """
    return getConfigValue("rdscore_addr")


def getDataDir() -> str:
    '''获取数据目录的绝对路径
    Returns:
        str: 数据目录路径
    '''
    if os.path.exists(getConfigValue("rdscore_data_dir")):
        return getConfigValue("rdscore_data_dir")
    else:
        print("file not exist")
        return ""



def getExeDir() -> str:
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


def getLogAfterT(fdir=None, t0=None):
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
    log_dict = sorted(log_dict.items(), key=lambda s: s[0], reverse=True)
    out_log = []
    for l in log_dict:
        if l[0] > t0:
            out_log.append(os.path.join(fdir, l[1]))
    return out_log


def openRDSCore(rdsDir=None):
    subprocess.call("rbk.exe", cwd=rdsDir, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)


def runRDSCore(rdsDir=None):
    p1 = multiprocessing.Process(target=openRDSCore, args=(rdsDir,))
    p1.daemon = True
    p1.start()
    return p1


def getLeasetLog(fdir=None):
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
    log_dict = sorted(log_dict.items(), key=lambda s: s[0], reverse=True)
    tf = os.path.join(fdir, log_dict[0][1])
    print(tf)
    return tf


class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OrderLib(metaclass=SingletonMetaClass):
    def __init__(self, ip) -> None:
        print("Create OrderLib")
        self.ip = ip
        self.tcp_ip = self.ip.split("/")[-1]
        self.tcp_ip = self.tcp_ip.split(":")[0]
        self.rbk = rbklib.rbklib(self.tcp_ip, True)
        self.OrderLibCom = OrderLibCom(ip=self.tcp_ip)
        self.time_tem = None

    def __del__(self):
        self.rbk.__del__()

    def selectOrder(self, order_id):
        r = requests.get(self.ip + "/orderDetails/{}".format(order_id), headers=_orderLif_headers)
        return r.json()

    def sendOrgOrder(self, order: str):
        r = requests.post(self.ip + "/setOrder", data=order, headers=_orderLif_headers)
        print(r.json())

    def fireOperations(self, flag: bool):
        d = json.dumps({"on": flag})
        r = requests.post(self.ip + "/fireOperations", data=d, headers=_orderLif_headers)
        print(r.json())

    def isFire(self):
        r = requests.get(self.ip + "/isFire", headers=_orderLif_headers)
        return r.json()

    def deleteOrder(self, order_id):
        """
            删除运单
        """
        d = json.dumps({"id": order_id})
        r = requests.post(self.ip + "/deleteOrder", data=d, headers=_orderLif_headers)
        print(r.json())

    def reNewOrder(self, order, uuid=None):
        """
            用于更新order中的orderId和blockId
        """
        if uuid == None:
            uuid = getUUID()
        bId = 0
        order["id"] = uuid
        for b in order["blocks"]:
            b["blockId"] = uuid + "_" + str(bId)
            bId += 1
        d = json.dumps(order)
        print(d)
        r = requests.post(self.ip + "/setOrder", data=d, headers=_orderLif_headers)
        return uuid

    def gotoOrder(self, vehicle=None, location=None, group=None, complete=True,
                  binTask=None, operation=None, operationArgs=None,
                  scriptName=None, scriptArgs=None, goodsId=None,
                  keyRoute=None,
                  sleepTime=None,
                  priority=None,
                  keyTask=None,
                  label=None,
                  prePointRedo=None):
        uuid = getUUID()
        if type(vehicle) is str:
            uuid = vehicle + ":" + uuid
        if location != None:
            datas = json.dumps(
                {
                    "blocks": [
                        {
                            "blockId": uuid + ":0",
                            "location": location,
                            "binTask": ("" if type(binTask) is not str else binTask),
                            "operation": ("" if type(operation) is not str else operation),
                            "operationArgs": ("" if type(operationArgs) is not dict else operationArgs),
                            "scriptName": ("" if type(scriptName) is not str else scriptName),
                            "scriptArgs": ("" if type(scriptArgs) is not dict else scriptArgs),
                            "goodsId": ("" if type(goodsId) is not str else goodsId)
                        }
                    ],
                    "priority": (0 if type(priority) is not int else priority),
                    "complete": complete,
                    "id": uuid,
                    "vehicle": ("" if type(vehicle) is not str else vehicle),
                    "group": ("" if type(group) is not str else group),
                    "label": ("" if type(label) is not str else label),
                    "keyRoute": (keyRoute if isinstance(keyRoute, str) or isinstance(keyRoute, list) else ""),
                    "keyTask": ("" if type(keyTask) is not str else keyTask),
                    "prePointRedo": (False if type(prePointRedo) is not bool else prePointRedo)
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
                    "keyRoute": ([] if type(keyRoute) is not list else keyRoute),
                    "keyTask": ("" if type(keyTask) is not str else keyTask),
                    "label": ("" if type(label) is not str else label),
                    "prePointRedo": (False if type(prePointRedo) is not bool else prePointRedo)
                }
            )
        print(datas)
        r = requests.post(self.ip + "/setOrder", data=datas, headers=_orderLif_headers)
        if sleepTime is not None:
            time.sleep(sleepTime)
        return uuid

    def sweepOrder(self,vehicle:str,workArea:str,oid:str=None)->str:
        """"""
        if oid is None:
            oid=getUUID()
        requests.post(self.ip + '/setOrder',json={ 'id': oid,'vehicle': vehicle,'workArea': workArea})
        return oid

    def sweeprobEvacuate(self,vehicles:list):
        """撤离清洁机器人"""
        return requests.post(self.ip + '/setCleanRobotEvacuation', json={ "vehicles": vehicles})

    def callCleanRobotBack(self,vehicles:list):
        """呼叫机器人返场"""
        return requests.post(self.ip + '/callCleanRobotBack', json={"vehicles": vehicles})

    def setShareOrder(self, **kwargs)->str:
        """下发标准仿真拼合运单
        :param kwargs:
            loc  load,unload任务位置
            operation load,unload,zero(复位),change(交换背篓)
            changePosition0 change位置1
            changePosition1 change位置2
            goodsId 货物id
            selfPosition 放货位置,注意是背篓位置
            priority 优先级
        """
        oid = getUUID()
        json_d = {
            'id': oid,
            'keyRoute': kwargs.get('loc'),
            'complete': True,
            'priority': kwargs.get('priority'),
            'vehicle':kwargs.get('vehicle'),
            'keyTask': kwargs.get('operation'),
            'blocks': [
                {
                    'blockId': oid + '01',
                    'location': kwargs.get('loc'),
                    "operation": "script",
                    "script_name": "ctuNoBlock.py",
                    "script_args": {
                        "operation": kwargs.get('operation')
                    }
                }
            ]
        }
        if kwargs.get('operation') == 'change':
            json_d['blocks'][0]['script_args']['changePosition0']=kwargs.get('changePosition0')
            json_d['blocks'][0]['script_args']['changePosition1']=kwargs.get('changePosition1')
        if kwargs.get('keyGoodsID') is not None:
            json_d['blocks'][0]['keyGoodsId']=kwargs.get('keyGoodsID')
        else:
            if kwargs.get('operation')=='load' or kwargs.get('operation')=='unload':
                json_d['blocks'][0]['goodsId'] = kwargs.get('goodsId') if kwargs.get('goodsId') else oid
                if kwargs.get('selfPosition'):
                    json_d['blocks'][0]['script_args']['selfPosition'] = kwargs.get('selfPosition')
        res=requests.post(url=f"{self.ip}/setOrder", json=json_d, timeout=10)
        print(res.json())
        return oid


    def sweepOrder(self):
        """"""


    def simpleOrder(self, fromLoc, toLoc, fromLoc2=None, toLoc2=None, goodsdId=None, LoadReport=None, UnloadReport=None,
                    vehicle=None):
        uuid = getUUID()
        data = {
            "fromLoc": fromLoc,
            "toLoc": toLoc,
            "id": uuid,
            "goodsId": ("" if type(goodsdId) is not str else goodsdId),
            "vehicle": ("" if type(vehicle) is not str else vehicle)
        }
        if fromLoc2 != None:
            data["fromLoc2"] = fromLoc2
        if toLoc2 != None:
            data["toLoc2"] = toLoc2
        if LoadReport != None:
            data["loadPostAction"] = {"configId": LoadReport}
        if UnloadReport != None:
            data["unloadPostAction"] = {"configId": UnloadReport}
        datas = json.dumps(data)
        print(datas)
        r = requests.post(self.ip + "/setOrder", data=datas, headers=_orderLif_headers)
        return uuid

    def addBlock(self, orderId=None, location=None,
                 binTask=None, operation=None, operationArgs=None,
                 scriptName=None, scriptArgs=None, goodsId=None,
                 sleepTime=None, complete=False):
        uuid = orderId + ":" + getUUID()
        blockId = uuid + ":0"
        datas = {
            "blocks": [
                {
                    "blockId": blockId,
                    "location": location,
                    "binTask": ("" if type(binTask) is not str else binTask),
                    "operation": ("" if type(operation) is not str else operation),
                    "operationArgs": ("" if type(operationArgs) is not dict else operationArgs),
                    "scriptName": ("" if type(scriptName) is not str else scriptName),
                    "scriptArgs": ("" if type(scriptArgs) is not dict else scriptArgs),
                    "goodsId": ("" if type(goodsId) is not str else goodsId)
                }
            ],
            "id": orderId,
        }
        if complete == True:
            datas["complete"] = True
        datas = json.dumps(datas)
        print(datas)
        r = requests.post(self.ip + "/addBlocks", data=datas, headers=_orderLif_headers)
        if sleepTime is not None:
            time.sleep(sleepTime)
        return blockId

    def manualFinishedCurrentBlock(self, name):
        datas = json.dumps(
            {
                "vehicles": [name]
            }
        )
        print("manualFinished: ", datas)
        r = requests.post(self.ip + "/manualFinished", data=datas, headers=_orderLif_headers)
        return r

    def robotsInCountGroup(self, name):
        datas = json.dumps(
            {
                "group": name
            }
        )
        print("robotsInCountGroup: ", datas)
        r = requests.post(self.ip + "/robotsInCountGroup", data=datas, headers=_orderLif_headers)
        return r

    def markComplete(self, orderId: str):
        datas = json.dumps(
            {
                "id": orderId
            }
        )
        print("markComplete: ", datas)
        r = requests.post(self.ip + "/markComplete", data=datas, headers=_orderLif_headers)
        return r

    def timeOut(self,time_out=60):
        """用于while True循环的超时计时"""
        if time.time()-self.time_tem>time_out:
            raise TimeoutError





    def terminateCurrentTask(self, vehicles, disableVehicle):
        datas = json.dumps(
            {
                "vehicles": [vehicles],
                "disableVehicle": disableVehicle
            }
        )
        r = requests.post(self.ip + "/terminate", data=datas, headers=_orderLif_headers)
        return r

    def unassignOrder(self, vehicle):
        datas = json.dumps(
            {
                "vehicle": vehicle
            }
        )
        r = requests.post(self.ip + "/unassignOrder", data=datas, headers=_orderLif_headers)
        return r

    def unassignOrderById(self, id):
        r = requests.post(self.ip + "/unassignOrder/" + id)
        return r

    def orderDetails(self, orderId):
        r = requests.get(self.ip + "/orderDetails/" + orderId)
        out = dict()
        try:
            out = json.loads(r.text)
        except:
            pass
        return out

    def devicesDetails(self):
        r = requests.get(self.ip + "/devicesDetails")
        out = dict()
        try:
            out = json.loads(r.text)
        except:
            pass
        return out

    def orders(self):
        r = requests.get(self.ip + "/orders")
        out = dict()
        try:
            out = json.loads(r.text)
        except:
            pass
        if "total" in out:
            params = {}
            params['size'] = out["total"]
        time.sleep(1)
        r = requests.get(self.ip + "/orders", params=params,
                         headers=_orderLif_headers)
        try:
            out = json.loads(r.text)
        except:
            pass
        return out

    def setOrderLabel(self, orderId, label):
        r = requests.post(self.ip + "/setLabel", data=json.dumps({"id": orderId, "label": label}),
                          headers=_orderLif_headers)
        return r

    def setOrderPriority(self, orderId, priority):
        r = requests.post(self.ip + '/setPriority', data=json.dumps({"id": orderId, "priority": priority}),
                          headers=_orderLif_headers)
        return r

    def terminateAll(self, vehicle):
        if isinstance(vehicle, str):
            datas = json.dumps(
                {
                    "vehicles": [vehicle],
                    "clearAll": True
                }
            )
            r = requests.post(self.ip + "/terminate", data=datas, headers=_orderLif_headers)
            return datas
        if isinstance(vehicle, list):
            datas = json.dumps(
                {
                    "vehicles": vehicle,
                    "clearAll": True
                }
            )
            r = requests.post(self.ip + "/terminate", data=datas, headers=_orderLif_headers)
            return datas
        return "wrong vehicle {}".format(vehicle)

    def terminateIdList(self, ids,disable_vehicle:bool=True):
        datas = json.dumps(
            {
                "idList": ids,
                "disableVehicle": disable_vehicle
            }
        )
        r = requests.post(self.ip + "/terminate", data=datas, headers=_orderLif_headers)
        return datas

    def terminateId(self, order_id, disableVehicle=None):
        if isinstance(disableVehicle, bool):
            datas = json.dumps(
                {
                    "id": order_id,
                    "disableVehicle": disableVehicle
                }
            )
        else:
            datas = json.dumps(
                {
                    "id": order_id
                }
            )
        r = requests.post(self.ip + "/terminate", data=datas, headers=_orderLif_headers)
        return datas

    def dispatchable_org(self, name, type_str, finished: bool = False):
        if type(name) is not list:
            name = [name]
        if name == "dispatchable":
            datas = json.dumps(
                {
                    "vehicles": name,
                    "type": type_str
                }
            )
        else:
            datas = json.dumps(
                {
                    "vehicles": name,
                    "type": type_str,
                    "finishedCurrentOrders": finished
                }
            )
        print(datas)
        r = requests.post(self.ip + "/dispatchable", data=datas, headers=_orderLif_headers)
        return r

    def undispatchable_unignore(self, name, finished=False):
        return self.dispatchable_org(name, "undispatchable_unignore", finished)

    def undispatchable_ignore(self, name, finished=False):
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
        r = requests.post(self.ip + "/lock", data=datas, headers=_orderLif_headers)
        return r

    def unlocked(self, name=None):
        if name is None:
            datas = json.dumps({
                "vehicles": []
            })
        else:
            if type(name) is not list:
                name = [name]
            datas = json.dumps({
                "vehicles": name
            })
        r = requests.post(self.ip + "/unlock", data=datas, headers=_orderLif_headers)
        return r

    def gotoSiteCancel(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps(
            {
                "vehicles": name
            }
        )
        r = requests.post(self.ip + "/gotoSiteCancel", data=datas, headers=_orderLif_headers)
        return r

    def gotoSitePause(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps({"vehicles": name})
        r = requests.post(self.ip + '/gotoSitePause', data=datas, headers=_orderLif_headers)
        return r

    def gotoSiteResume(self, name):
        if type(name) is not list:
            name = [name]
        datas = json.dumps({"vehicles": name})
        r = requests.post(self.ip + '/gotoSiteResume', data=datas, headers=_orderLif_headers)
        return r

    def uploadScene(self, name: str = ""):
        p = os.path.dirname(__file__)
        p = os.path.dirname(p)
        scene_path = os.path.join(p, name)
        start_time = time.time()
        with open(scene_path, 'rb') as f:
            datas = f.read()
            r = requests.post(self.ip + "/uploadScene", data=datas)
            print(r.status_code)
            while r.status_code == 400:
                self.terminateAllOrder()
                r = requests.post(self.ip + "/uploadScene", data=datas)
                print("reupdate", r.status_code)
                time.sleep(10)
            if r.status_code == 200:
                print(f"upload successful! timecost: {(time.time()-start_time):.2f} seconds")
        return r

    def waitForOrderFinish(self, uuid,timeout=60):
        status = "RUNNING"
        time_elapsed=0
        while status != "FINISHED" and status != "STOPPED":
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            # print("waitForOrderFinish", uuid, out, status)
            time.sleep(1)
            time_elapsed+=1
            if time_elapsed>timeout:
                # print(f"order haven't finished after {time_elapsed},",json.dumps(out,indent=4))
                raise TimeoutError("order not finished in expected time")
        return True

    def waitForOrderWaitTimeout(self, uuid, timeout=30):
        status = "RUNNING"
        time_elapsed = 0
        while status != "FINISHED" \
                and status != "STOPPED" \
                and status != "WAITING":
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("waitForOrderFinish", uuid, out, status)
            time.sleep(1)
            time_elapsed += 1
            print(time_elapsed)
            if time_elapsed > timeout:
                print("waitForOrderWATING", uuid, out, status, "TIMEOUT")
                return False
        return True

    def getOrderState(self, uuid):
        out = self.orderDetails(uuid)
        state = "UNKNOW"
        if type(out) is dict and "state" in out:
            state = out["state"]
        return state

    def getOrderError(self, oid):
        out = self.orderDetails(oid)
        error = []
        if type(out) is dict and 'errors' in out:
            error = out['errors']
        return error

    def getBlockState(self,uuid):
        """查询动作块状态"""
        out = self.orderDetails(uuid)
        state = "UNKNOW"
        if type(out) is dict and "state" in out:
            state = out["blocks"][-1]["state"]
        return state

    def getFinalPath(self,vehicle,timeout=60)->dict:
        """获取运单完成路径"""
        final_path = {}
        if isinstance(vehicle,str):
            vehicle=[vehicle]
        count=0
        path_tem=[]
        ismove={v:False for v in vehicle}
        for _ in range(timeout):
            time.sleep(1)
            for i in  range(0,len(vehicle)):
                path_tem = self.get_finished_path(vehicle_id=vehicle[i])
                if path_tem == [] and final_path.get(vehicle[i]):
                    if not ismove[vehicle[i]]:
                        ismove[vehicle[i]] = True
                        continue
                    else:
                        ismove[vehicle[i]]=True
                        count+=1
                        break
                else:
                    final_path[vehicle[i]] = path_tem
            print("final_path",final_path)
            if count>=len(vehicle):
                break
        else:
            raise TimeoutError("vehicle might have not finished order")
        return final_path

    def getClearFinalPath(self,vehicle,timeout=60) -> dict:
        """获取没有避让下的运单完成路径"""
        final_path=[]
        for _ in range(timeout):
            time.sleep(1)
            path_tem = self.get_finished_path(vehicle_id=vehicle)
            if path_tem == []:
                break
            else:
                final_path = path_tem
        else:
            raise TimeoutError("vehicle might have not finished order")
        if final_path !=[]:
            print(final_path)
            final_path_todict={}
            for i in range(len(final_path)):
                if final_path_todict.get(final_path[i]) is None:
                    final_path_todict[final_path[i]]=i
                else:
                    raise ValueError(f"path has duplicate value {final_path[i]}")
            return final_path_todict
        else:
            return {}

    def getAvoidpath(self,expected_path,real_path)->list:
        """获取避让路径
        params:
        expected_path : dict 无避让下的路径, 可以通过 getClearFinalPath() 获取
        real_path: list  实际的路径
        """
        indexl=0
        indexr=0  # 递增点位指针, 指向点位不能"减少"
        flag=False  # 绕路标志, 如果绕路, 值为true
        avoid_paths=[]
        for i in range(len(real_path)):
            if expected_path.get(real_path[i]) is not None:
                if flag==True:
                    if indexr<i:
                        avoid_paths.append(real_path[indexl:i+1])
                        flag=False
                    else:
                        continue
                elif i<indexr :
                    indexl = indexr
                    flag=True
                else:
                    indexr=i
            else:
                if flag==False:
                    indexl = indexr
                    flag=True
        return avoid_paths



    def waitForOrderFinishTimeout(self, uuid, timeout=30) -> bool:
        status = "RUNNING"
        time_elapsed = 0
        while status != "FINISHED" and status != "STOPPED":
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("waitForOrderFinish", uuid, out, status)
            time.sleep(1)
            time_elapsed += 1
            print(time_elapsed)
            if status=="FAILED":
                return False
            if time_elapsed > timeout:
                print("waitForOrderFinish", uuid, out, status, "TIMEOUT")
                return False
        return True

    def waitForOrderWaitingTimeOut(self, uuid, timeout=30) -> bool:
        status = 'RUNNING'
        time_elapsed = 0
        while status != 'WAITING':
            out = self.orderDetails(uuid)
            if type(out) is dict and 'state' in out:
                status = out['state']
            print("waitForOrderWaiting", uuid, out, status)
            time.sleep(1)
            time_elapsed += 1
            print(time_elapsed)
            if time_elapsed > timeout:
                print("waitForOrderWaiting", uuid, out, status, "TIMEOUT")
                return False
        return True

    def getRobotPosition(self, vehicle):
        return self.robotStatus(vehicle)['rbk_report']['current_station']

    def isOrderFinished(self, uuid, timeout=30):
        status = "RUNNING"
        time_elapsed = 0
        while status != "FINISHED" and status != "STOPPED":
            out = self.orderDetails(uuid)
            if type(out) is dict and "state" in out:
                status = out["state"]
            print("isOrderFinished", uuid, out, status)
            time.sleep(1)
            time_elapsed += 1
            print(time_elapsed)
            if time_elapsed > timeout:
                print("TIMEOUT")
                return False
            if status == "FINISHED":
                return True
            if status == "STOPPED":
                return False

    def init_pos(self, loc: str, name: str, a=None, map=None):
        """ 移动机器人到某个站点，朝向为a，单位为rad
        """
        data = {
            "vehicle_id": name,
            "fail_current_task": True
        }
        self.updateSimRobotState(json.dumps(data))
        time.sleep(0.5)
        self.terminateAll(vehicle=name)
        self.undispatchable_ignore(name=name)
        data = {
            "vehicle_id": name,
            "position_by_name": loc
        }
        if type(a) == float or type(a) == int:
            data["angle"] = a
        if type(map) == str:
            data["position_map"] = map
        self.updateSimRobotState(json.dumps(data))
        self.locked()
        time.sleep(0.5)
        self.clearRobotAllError(name)
        self.dispatchable(name=name)
        time.sleep(0.5)

    def init_pos_str(self, x: float, y: float, name: str, a=None, map=None):
        """ 移动机器人到某个位置，朝向为a，单位为rad
        """
        data = {
            "vehicle_id": name,
            "fail_current_task": True
        }
        self.updateSimRobotState(json.dumps(data))
        time.sleep(1)
        self.terminateAll(vehicle=name)
        self.dispatchable(name=name)
        position_str = json.dumps({"x": x, "y": y})
        data = {
            "vehicle_id": name,
            "position": position_str
        }
        if type(a) == float:
            data["angle"] = a
        if type(map) == str:
            data["position_map"] = map
        self.updateSimRobotState(json.dumps(data))
        self.locked()
        time.sleep(1)
        self.clearRobotAllError(name)
        self.dispatchable(name=name)
        time.sleep(1)

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
        r = requests.post(self.ip + "/clearRobotAllError", data=datas, headers=_orderLif_headers)
        return r

    def getPing(self):
        r = requests.get(self.ip + "/ping")
        return r.json()

    # roboview
    def roboviewPyTest(self, datas):
        r = requests.post(self.ip + "/pyTest", data=datas, headers=_orderLif_headers)
        return r.json()

    def robotsStatus(self):
        r = requests.get(self.ip + "/robotsStatus")
        return r.json()

    def getCurrentOrderId(self, vehicle_id: str):
        rs = self.robotStatus(vehicle_id)
        if "id" in rs["current_order"]:
            return rs["current_order"]["id"]
        return ""

    def getCoreError(self):
        rs = self.robotsStatus()
        return rs['alarms']['errors']

    def getCoreWarning(self):
        rs = self.robotsStatus()
        return rs['alarms']['warnings']

    def robotStatus(self, vehicle_id: str):
        data = dict()
        rs = self.robotsStatus()
        for r in rs["report"]:
            if r["uuid"] == vehicle_id:
                data = r
                break
        return data

    def get_robot_coordinate(self, vehicle_id: str):
        """获取机器人当前点位和坐标"""
        res = requests.get(url=f"{self.ip}/robotsStatus")
        for r in res.json()["report"]:
            if r["vehicle_id"] == vehicle_id:
                return (r["rbk_report"]["current_station"], r["rbk_report"]["x"], r["rbk_report"]["y"])
        else:
            return f"can't find robot named {vehicle_id}"

    def get_robot_occupy(self, vehicle_id:str):
        """获取占用点位和线路以及当前时间戳"""
        res = requests.get(url=f"{self.ip}/robotsStatus")
        for r in res.json()["report"]:
            if r["vehicle_id"] == vehicle_id:
                return r["area_resources_occupied"][0]["path_occupied"]
        else:
            return f"can't find robot named {vehicle_id}"



    def get_finished_path(self, vehicle_id: str):
        """
        获取机器人走过的路线
        :return: list
        """
        data = self.robotStatus(vehicle_id)
        result: list = data.get('finished_path')
        return result

    def get_unfinished_path(self, vehicle_id: str):
        """
        获取机器人未来的路线
        :return: list
        """
        data = self.robotStatus(vehicle_id)
        result = data['unfinished_path']
        return result

    def get_current_station(self, vehicle_id: str):
        """
        获取机器人当前站点位置
        :return: str
        """
        data = self.robotStatus(vehicle_id)
        result = data['rbk_report']['current_station']
        return result

    def get_finished_path_while_arrive_penultimate_point(self, vehicle_x: str, penultimate_x: str, vehicle_y: str,
                                                         penultimate_y: str) -> [list, list]:
        done_x = done_y = False
        pos_x = pos_y = ""
        finished_path_x = finished_path_y = []
        while not done_x or not done_y:
            if not done_x:
                pos_x = self.getRobotPosition(vehicle_x)
            if not done_y:
                pos_y = self.getRobotPosition(vehicle_y)
            if pos_x == penultimate_x:
                finished_path_x = self.get_finished_path(vehicle_x)
                done_x = True
                pos_x = ""
            if pos_y == penultimate_y:
                finished_path_y = self.get_finished_path(vehicle_y)
                done_y = True
                pos_y = ""
            time.sleep(1)
        finished_path_x = [finished_path_x[i] for i in range(len(finished_path_x)) if i == 0 or finished_path_x[i] !=
                           finished_path_x[i - 1]]
        finished_path_y = [finished_path_y[i] for i in range(len(finished_path_y)) if i == 0 or finished_path_y[i] !=
                           finished_path_y[i - 1]]
        return [finished_path_x, finished_path_y]

    def updateSimRobotState(self, datas: str):
        """设置仿真机器人参数

        Args:
            datas (str): 这个json见文档，需要传入dump结果
            https://books.seer-group.com/public/rdscore/master/zh/api/http/robot/updateSimRobotState.html
            https://seer-group.yuque.com/pf4yvd/gp9mgx/xmyicq
        """
        r = requests.post(self.ip + "/updateSimRobotState", data=datas, headers=_orderLif_headers)
        return r

    def modifyParam(self, data: dict()):
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
    def modifyParamNew(self, data):
        """
        新版本的core，用http设置参数
        """
        r = requests.post(self.ip+"/saveCoreParam", json = data)
        print(r.content)

    def recoveryParam(self):
        self.rbk.recoveryParam()

    def recoverParamNew(self):
        r = requests.post(self.ip + "/reloadCoreParam", json = {})

    def disableDoor(self, names: list, disabled: bool):
        datas = json.dumps(
            {
                "names": names,
                "disabled": disabled
            }
        )
        r = requests.post(self.ip + "/disableDoor", data=datas, headers=_orderLif_headers)
        return r

    def disableLift(self, names: list, disabled: bool):
        datas = json.dumps(
            {
                "names": names,
                "disabled": disabled
            }
        )
        r = requests.post(self.ip + "/disableLift", data=datas, headers=_orderLif_headers)
        return r

    def disablePath(self, name: str):
        datas = json.dumps(
            {
                "id": name
            }
        )
        r = requests.post(self.ip + "/disablePath", data=datas, headers=_orderLif_headers)
        return r

    def disablePoint(self, name: str):
        datas = json.dumps(
            {
                "id": name
            }
        )
        r = requests.post(self.ip + "/disablePoint", data=datas, headers=_orderLif_headers)
        return r

    def enablePath(self, name: str):
        datas = json.dumps(
            {
                "id": name
            }
        )
        r = requests.post(self.ip + "/enablePath", data=datas, headers=_orderLif_headers)
        return r

    def enablePoint(self, name: str):
        datas = json.dumps(
            {
                "id": name
            }
        )
        r = requests.post(self.ip + "/enablePoint", data=datas, headers=_orderLif_headers)
        return r

    def getDisablePoints(self):
        r = requests.get(self.ip + "/getDisablePoints", headers=_orderLif_headers)
        return r.json()

    def getDisablePaths(self):
        r = requests.get(self.ip + "/getDisablePaths", headers=_orderLif_headers)
        return r.json()

    def pagedQuery(self, path: str, page_num: int = None, page_size: int = None, order_by: str = None,
                   order_method: str = None, relation: str = None, predicates: List[str] = None):
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

        r = requests.get(self.ip + "/" + path, params=params,
                         headers=_orderLif_headers)
        return r.json()

    def getLift(self, name: str):
        res = self.OrderLibCom.devices_details("lifts")
        lfs = res.json()["lifts"]
        for l in lfs:
            if l["name"] == name:
                return l
        return dict()

    def getDoor(self, name: str):
        res = self.OrderLibCom.devices_details("doors")
        ds = res.json()["doors"]
        for d in ds:
            if d["name"] == name:
                return d
        return dict()

    def doorStatus(self, door_name: str, timeout_seconds = 10):
        for _ in range(timeout_seconds):
            res = self.OrderLibCom.devices_details("doors")
            all_doors = res.json()["doors"]
            #https://stackoverflow.com/a/2361495/7724731
            target_door = None
            for target_door in (d for d in all_doors if d["name"] == door_name): break
            if target_door:
                print(f"Found door {door_name}")
                return target_door["doorstatus"]
            time.sleep(1)

        print(f"Timeout {door_name}")
        # TODO 超时的处理
        return None

    def terminateAllOrder(self):
        order_list = self.orders()
        # print(order_list)
        if "list" in order_list:
            ids = []
            for o in order_list["list"]:
                ids.append(o["id"])
            self.terminateIdList(ids)

    def assure_pos(self, vehicle_id: str, pos: str, timeout_sec: int = 60):
        """
        等到仿真机器人在指定位置，会阻塞，超时会抛出异常。
        解决上传场景后，core暂时处于不可用状态的问题
        @param vehicle_id: 机器人id
        @param pos: 目标位置
        @param timeout_sec: 等待超时时间
        @return: None
        """
        for _ in range(timeout_sec):
            time.sleep(1)
            status = self.robotStatus(vehicle_id)
            if status is None:
                continue
            # TODO 更精细的检查
            if "area_resources_occupied" not in status:
                continue
            res_occupied = status["area_resources_occupied"]
            if "path_occupied" not in res_occupied:
                continue
            path_occupied = res_occupied["path_occupied"]
            start_pos = path_occupied["start_id"]
            end_pos = path_occupied["end_id"]
            if start_pos == pos or end_pos == pos:
                return
            self.init_pos(loc=pos, name=vehicle_id)
        raise Exception(f"Assure pos timeout, vehicle_id: '{vehicle_id}', pos: '{pos}'")

    def waitUntilSceneUpdated(self, test_vehicle_id: str, test_pos1: str, test_pos2: str, timeout_sec: int = 60):
        """
        等待场景更新完成。
        判断场景更新完成的方法：
        1. 关闭 AutoPark 和 AutoCharge
        2. 将 test_vehicle_id 放在 test_pos1, 判断是否成功
        3. 将 test_vehicle_id 放在 test_pos2, 判断是否成功
        同一辆车放两个位置是解决机器人之前就在这个位置的情况导致的问题
        """
        start_time = time.time()
        self.modifyParam({"RDSDispatcher": {"AutoPark": False}})

        def test_pos(pos: str) -> bool:
            status = self.robotStatus(test_vehicle_id)
            if status is None:
                print("status None")
                return False
            if "area_resources_occupied" not in status:
                print("area_resources_occupied not found")
                return False
            res_occupied_list = status["area_resources_occupied"]
            print(res_occupied_list)
            if not res_occupied_list:
                print("area_resources_occupied is empty list")
                return False
            for res_occupied in res_occupied_list:
                if "path_occupied" not in res_occupied:
                    print("path_occupied not found")
                    continue
                path_occupied_list = res_occupied["path_occupied"]
                if not path_occupied_list:
                    print("path_occupied is empty list")
                    self.dispatchable(test_vehicle_id)
                    continue
                for path_occupied in path_occupied_list:
                    start_pos = path_occupied["source_id"]
                    end_pos = path_occupied["end_id"]
                    # TODO 更精细的检查
                    print(f"{test_vehicle_id}: {start_pos}->{end_pos}")
                    if start_pos == pos or end_pos == pos:
                        return True
            self.updateSimRobotState(datas=json.dumps({
                "vehicle_id": test_vehicle_id,
                "position_by_name": pos, }
            ))
            return False

        pos1_done = False
        pos2_done = False
        tick = 0
        while tick < timeout_sec:
            time.sleep(1)
            if not pos1_done:
                pos1_done = test_pos(test_pos1)
                tick+=1
                continue
            if not pos2_done:
                pos2_done = test_pos(test_pos2)
                tick+=1
                continue
            print(f"Scene updated. Waited for {(time.time() - start_time):.2f} seconds")
            return
        raise Exception("Timeout waiting update scene")

    def restart_core(self,interval: int=3):
        """用于重启windows版本的core,需要第三方库psutil
        :param : time, 重启间隔时间
        """
        def get_exe_path(process_name):
            for proc in psutil.process_iter(['name', 'exe']):
                if proc.info['name'] == process_name:
                    return proc.info['exe']
            return None
        core_path = get_exe_path("rbk.exe")
        print(core_path)
        # 重启core
        res = os.system('taskkill /F /IM rbk.exe')
        assert res == 0, "Failed to kill core"
        directory = os.path.dirname(core_path)
        print("restart core")
        time.sleep(interval)
        subprocess.call("start rbk.exe", cwd=directory, shell=True)

    def setupMAPF(self,RobotVision=None,LimitReplan=None,Undirected=None,AutoStrategy=None,AutoRecover=None,DefaultParameters=None) ->bool:
        """一键配置G-MAPF
        参数配置可能随版本变化"""
        res = requests.post(url=f"{self.ip}/setupMAPF", json={"type": "getMAPF"})
        print(json.dumps(res.json(), indent=4))
        default_param={}
        for i in res.json()['MAPF']:
            default_param.setdefault(i['key'],i['value'])
        if RobotVision is not None :
            default_param['RobotVision']=RobotVision
        if LimitReplan is not None :
            default_param['LimitReplan']=LimitReplan
        if Undirected is not None:
            default_param['Undirected']=Undirected
        if AutoStrategy is not None:
            default_param['AutoStrategy']=AutoStrategy
        if AutoRecover is not None:
            default_param['AutoRecover']=AutoRecover
        if DefaultParameters is not None:
            default_param['DefaultParameters']=DefaultParameters
        data = {'data': [], 'type': 'setMAPF'}
        for key,value in default_param.items():
            data['data'].append({'key': key, 'value': value})
        print(json.dumps(data, indent=4))
        res = requests.post(url=f"{self.ip}/setupMAPF", json=data)
        return res.status_code==200

    def set_param(self,param_path,table="RDSDispatcher",recover=True):
        """根据现场 robot.param 一键配置参数,默认仅配置"RDSDispatcher",
        :param : param_path robot.param路径
        注意: 旧版MAPF开头的参数新版改为 G-MAPF开头的参数, 失败的参数可以在输出中用"failed modify"搜索,请认真核对
        """
        if recover:
            self.recoveryParam()
            time.sleep(2)
        param_to_dict = {"RDSDispatcher":{}}
        sql3 = sqlite3.connect(param_path)
        cursor = sql3.cursor()
        er_list = [] # 保存由于版本不符不存在的参数
        try:
            cursor.execute(f"select * from {table}")
            sql3.commit()
        except Exception:
            sql3.close()
            raise sqlite3.DatabaseError
        try:
            count=0
            data=cursor.fetchall()
            for i in data:
                if i[1]=='b' or i[1]=='bool':
                    # print(i)
                    if i[2]=="1":
                        param_to_dict[table].setdefault(i[0], True)
                    else:
                        param_to_dict[table].setdefault(i[0], False)
                    count+=1
                elif i[1]=='d' or i[1]=='double':
                    param_to_dict[table].setdefault(i[0], float(i[2]))
                    count += 1
                elif i[1]=='i' or i[1]=='int' or i[1]=="j":
                    param_to_dict[table].setdefault(i[0], int(float(i[2])))
                    count += 1
                elif 'char' in i[1]:
                    param_to_dict[table].setdefault(i[0], i[2])
                    count += 1
                else:
                    raise TypeError("unknown type")
                if count>20:
                    count=0
                    self.modifyParam(data=param_to_dict)
                    param_to_dict[table]={}
            self.modifyParam(data=param_to_dict)
            for change in range(2):
                time.sleep(3)
                dt = json.loads(self.rbk.robot_status_params_req(plugin=table)[1].decode())
                print("dt:",dt)
                for i in data:
                    if dt[table].get(i[0]) is None:
                        if change == 1:
                            er_list.append(i[0])
                        continue
                    if i[1] == 'b' or i[1] == 'bool':
                        # print(i)
                        if i[2] == "1":
                            if dt[table][i[0]]["value"]== True:
                                continue
                            else:
                                self.modifyParam(data={table: {i[0]: True}})
                                if change==1:
                                    print("set param error:",i[0],i[2],dt[table][i[0]]["value"])
                        else:
                            if dt[table][i[0]]["value"] == False:
                                continue
                            else:
                                self.modifyParam(data={table: {i[0]: False}})
                                if change == 1:
                                    print("set param error:",i[0], i[2],dt[table][i[0]])
                    elif i[1] == 'd' or i[1] == 'double':
                        if dt[table][i[0]]["value"] == float(i[2]):
                            continue
                        else:
                            self.modifyParam(data={table: {i[0]: float(i[2])}})
                            if change == 1:
                                print("set param error:",i[0], i[2], dt[table][i[0]])
                    elif i[1] == 'i' or i[1] == 'int' or i[1]=="j":
                        if dt[table][i[0]] ["value"]== int(float(i[2])):
                            continue
                        else:
                            self.modifyParam(data={table: {i[0]: int(float(i[2]))}})
                            if change == 1:
                                print("set param error:",i[0], i[2], dt[table][i[0]])
                    elif 'char' in i[1]:
                        if dt[table][i[0]]["value"] == i[2]:
                            continue
                        else:
                            self.modifyParam(data={table: {i[0]: i[2]}})
                            print("set param error:", i[0],i[2], dt[table][i[0]])
                    else:
                        raise TypeError("unknown type")
            if er_list != []:
                raise Exception(f"param not exist {er_list}")
        except Exception as e:
            print("failed modify", e)
            sql3.close()
        sql3.close()


    def compare_param(self,param_path,set_mapf:bool=False):
        """现场参数,与当前一键配置g-mapf参数对比, 打印不同之处
        :param : set_mapf 是否一键配置mapf
        """
        difference=[]
        if set_mapf:
            self.setupMAPF()
            time.sleep(5)
        res2 = self.rbk.robot_status_params_req(plugin="RDSDispatcher")
        mapf_default = json.loads(res2[1].decode('utf-8'))
        # print(json.dumps(mapf_default,indent=4))
        sql3 = sqlite3.connect("robot.param")
        cursor = sql3.cursor()
        try:
            cursor.execute("select * from RDSDispatcher")
            sql3.commit()
        except Exception:
            sql3.close()
            raise sqlite3.DatabaseError
        try:
            count = 0
            data = cursor.fetchall()
            for i in data:
                # print(i)
                if i[1]=='b' or i[1]=='bool':
                    if i[2]=="1":
                        if str(mapf_default["RDSDispatcher"].get(i[0]).get("value"))==True:
                            continue
                        else:
                            difference.append(i[0])
                    if i[2]=="0":
                        if str(mapf_default["RDSDispatcher"].get(i[0]).get("value")) == False:
                            continue
                        else:
                            difference.append(i[0])
                elif  str(mapf_default["RDSDispatcher"].get(i[0]).get("value"))==i[2]:
                    continue
                else:
                    difference.append(i[0])

        except Exception as e:
            print(e)
        print("difference:",difference)

    def undispatchable_ignore_without_order(self,order_path:str=None,filter:dict= None,order_table:str="Order",vehicles:list=None):
        """将数据库没有运单的车设为undispatchable_ignore
        :param : order_path  orders.sqlite的路径
        :param : filter  需要过滤的数据,只能精确匹配,参考方法  order_redo()
                举个栗子: 传入参数 filter={"state": ("STOPPED", "FINISHED"), "receive_time": (1701588666, 1701589866), "vehicle": ("AMB-01")}
                        表示筛选运单状态为 "STOPPED" 或 "FINISHED", 发送运单时间在1701588666到1701589866 之间, 指定车为"AMB-01" 的运单
        :param : order_table  需要恢复的运单表,可选的表有AreaToAreaOrder, DistributeOrder, Order, SimpleOrder, SweepOrder
        """
        sql3 = sqlite3.connect(order_path)
        sql3.row_factory = sqlite3.Row
        cursor = sql3.cursor()
        sql_query = f"select distinct vehicle from {repr(order_table)}"
        filter.setdefault("type", "0")  # 默认只有非自动任务
        if filter:
            sql_query += " where"
            first_flag = True
            for i, j in filter.items():
                print(i, j)
                if first_flag:
                    first_flag = False
                else:
                    sql_query += " and"
                if i == "terminate_time" or i == "create_time" or i == "receive_time":
                    if not j:
                        sql_query += f" {i} between 0 and {int(time.time())}"
                    else:
                        if isinstance(j[0],str):
                            if len(j[0].split(":")) == 4:
                                date_format = "%Y-%m-%d %H:%M:%S"
                                j0 = datetime.strptime(j[0], date_format)
                                j1 = datetime.strptime(j[1], date_format)
                                j0_s = int(time.mktime(j0.timetuple()))
                                j1_s = int(time.mktime(j1.timetuple()))
                                sql_query += f" {i} between {j0_s} and {j1_s}"
                            else:
                                raise Exception(f"time format is not standard, {j}")
                        else:
                            sql_query += f" {i} between {j[0]} and {j[1]}"
                else:
                    if isinstance(j, str):
                        sql_query += f" {i}=={repr(j)}"
                    else:
                        sql_query += f" {i} in {repr(j)}"
        sql_query += " order by receive_time"
        print("sql:", sql_query)
        try:
            cursor.execute(sql_query)
            sql3.commit()
            data = cursor.fetchall()
            data_dcit = [dict(row) for row in data]
            vehicle_li = []
            for i in data_dcit:
                vehicle_li.append(i.get("vehicle"))
            dis_v=[]
            for v in vehicles:
                if v not in vehicle_li:
                    dis_v.append(v)
            self.undispatchable_ignore(dis_v)
        except Exception as e:
            print(e)
            sql3.close()
        finally:
            sql3.close()



    def order_redo(self,order_path:str=None,filter:dict= None,order_table="Order",send_type=1,interval=10,amount=None,specified_vehicle:int=1):
        """重做数据库的运单
        :param : order_path  orders.sqlite的路径

        :param : filter  需要过滤的数据,只能精确匹配,目前支持的字段有    id
                                                                state, 运单状态, 如 FINISHED STOOPED WAITING FAILED
                                                                time(terminate_time,create_time,receive_time), 格式为 Unix时间戳,或者 年-月-日 时:分:秒
                                                                vehicle,
                                                                type,  0表示非自动任务, 1,2,3表示自动任务, 默认为0
                                                                group_name,
                                                                order_odo 运单里程等
                举个栗子: 传入参数 filter={"state": ("STOPPED", "FINISHED"), "receive_time": (1701588666, 1701589866), "vehicle": ("AMB-01")}
                        表示筛选运单状态为 "STOPPED" 或 "FINISHED", 发送运单时间在1701588666到1701589866 之间, 指定车为"AMB-01" 的运单
        :param : order_table  需要恢复的运单表,可选的表有AreaToAreaOrder, DistributeOrder, Order, SimpleOrder, SweepOrder
        :param : send_type  1 默认值,一次下发所有运单
                            2 按receive_time间隔发单
                            3 每间隔 interval发送一个运单
        :param : amount     是否需要限定下发的运单数量, 默认否
        :param : specified_vehicle 是否所有运单按照数据库的运单分配,
                                    1 按照数据库的运单分配指定车,默认值
                                    2 通过调度分配,只在user_specified_vehicle指定车时时指定
                                    3 所有运单都通过调度分配
        """
        sql3 = sqlite3.connect(order_path)
        sql3.row_factory=sqlite3.Row
        cursor = sql3.cursor()
        sql_query=""
        if specified_vehicle==1 or specified_vehicle==2:
            sql_query=f"select vehicle,group_name,label_name,block_id_list,priority,key_route,receive_time,user_specified_vehicle from {repr(order_table)}"
        else:
            sql_query = f"select vehicle,group_name,label_name,block_id_list,priority,key_route,receive_time from {repr(order_table)}"
        filter.setdefault("type","0")   # 默认只有非自动任务
        if filter:
            sql_query +=" where"
            first_flag=True
            for i,j in filter.items():
                print(i,j)
                if first_flag:
                    first_flag=False
                else:
                    sql_query +=" and"
                if i=="terminate_time" or i=="create_time" or i=="receive_time":
                    if not j:
                        sql_query += f" {i} between 0 and {int(time.time())}"
                    else:
                        if isinstance(j[0],str):
                            if j[0].find(":"):  # 时间格式未作清晰的检查
                                date_format = "%Y-%m-%d %H:%M:%S"
                                j0 = datetime.strptime(j[0], date_format)
                                j1 = datetime.strptime(j[1], date_format)
                                j0_s = int(j0.timestamp())
                                j1_s = int(j1.timestamp())
                                # j0_s = calendar.timegm(j0.timetuple())
                                # j1_s = calendar.timegm(j1.timetuple())
                                sql_query+=f" {i} between {j0_s} and {j1_s}"
                            else:
                                raise Exception(f"time format is not standard, {j}")
                        else:
                            sql_query += f" {i} between {j[0]} and {j[1]}"

                else:
                    if isinstance(j,str):
                        sql_query += f" {i}=={repr(j)}"
                    else:
                        sql_query += f" {i} in {repr(j)}"
        sql_query+=" order by receive_time"
        if amount:
            sql_query += f" limit {amount}"

        print("sql:",sql_query)
        try:
            cursor.execute(sql_query)
            sql3.commit()
        except Exception as e:
            print(e)
            sql3.close()
        # 发单
        try:
            data = cursor.fetchall()
            data_dcit=[dict(row) for row in data]
            start_time=None
            print("order totals:",len(data_dcit))
            for i in data_dcit:
                if not start_time:
                    start_time=i['receive_time']
                order_dt={}
                order_dt["id"]=f"{i['vehicle']}:"+str(uuid.uuid1())
                # print(i)
                if specified_vehicle==1:
                    if i["vehicle"] :
                        order_dt.setdefault("vehicle",i["vehicle"])
                elif specified_vehicle==2:
                    if i["vehicle"] and i["user_specified_vehicle"]:
                        order_dt.setdefault("vehicle", i["vehicle"])
                if i["group_name"]:
                    order_dt.setdefault("group",i["group_name"])
                if i["label_name"]:
                    order_dt.setdefault("label",i["label_name"])
                if i["priority"]:
                    order_dt.setdefault("priority",i["priority"])
                if i["key_route"]:
                    order_dt.setdefault("keyRoute",i["key_route"])
                block_count=0
                if i['block_id_list']:
                    for block in i['block_id_list'].split(','):
                        cursor.execute(f"select * from Block where id=={repr(block)}")
                        sql3.commit()
                        block_data=cursor.fetchall()
                        block_data_dict=[dict(row) for row in block_data]
                        if block_data_dict==[]:
                            continue
                        # print("block_data_dict",block_data_dict)
                        order_dt.setdefault("blocks", []).append({})
                        if block_data_dict[0]['location']:
                            order_dt.get("blocks")[block_count].setdefault('location',block_data_dict[0]['location'])
                        if block_data_dict[0]['operation']:
                            order_dt.get("blocks")[block_count].setdefault('operation',block_data_dict[0]['operation'])
                        order_dt.get("blocks")[block_count].setdefault('blockId', order_dt["id"]+":"+str(block_count))
                        block_count+=1
                        order_dt.setdefault("complete",True)
                if block_count == 0:
                    continue
                print(f"order_dt", order_dt)
                if send_type==2:
                    print("time.sleep", i["receive_time"] - start_time)
                    time.sleep(i["receive_time"]-start_time)
                    start_time=i["receive_time"]
                if send_type==3:
                    print("time.sleep", interval)
                    time.sleep(interval)
                requests.post(url=f"{self.ip}/setOrder",json=order_dt)
        except Exception as e:
            print("error",e)
        finally:
            sql3.close()

    def addBlock_redo(self, order_path, filter: dict = None, order_table="Order", addblock_type=1, range_t:int=-1,amount:int=None, undispatchable_idle=True):
        """重做数据库的运单,在完成运单后下发下一运单
        :param : order_path  orders.sqlite的路径
        :param : filter  需要过滤的数据,只能精确匹配,目前支持的字段有    id
                                                                state, 运单状态, 如 FINISHED STOOPED WAITING FAILED
                                                                time(terminate_time,create_time,receive_time), 格式为 Unix时间戳,或者 年-月-日 时:分:秒
                                                                vehicle,
                                                                type,  0表示非自动任务, 1,2,3表示自动任务, 默认为0
                                                                group_name,
                                                                order_odo 运单里程等
                举个栗子: 传入参数 filter={"state": ("STOPPED", "FINISHED"), "receive_time": (1701588666, 1701589866), "vehicle": ("AMB-01")}
                        表示筛选运单状态为 "STOPPED" 或 "FINISHED", 发送运单时间在1701588666到1701589866 之间, 指定车为"AMB-01" 的运单
        :param : order_table  需要恢复的运单表,可选的表有AreaToAreaOrder, DistributeOrder, Order, SimpleOrder, SweepOrder
        :param : addblock_type  1 默认值,一次下发所有动作块
                                2 动作块完成后追加下一动作块
                                3 # todo 自适应判断是否追加
        :param : undispatchable_idle  是否要将无任务的机器人设置为不可接单不占用资源
        :param : range  下发运单时间的最大极差, 默认无极差
        """
        # order_q=
        sql3 = sqlite3.connect(order_path)
        sql3.row_factory = sqlite3.Row
        cursor = sql3.cursor()
        sql_query_all = f"select id,vehicle,group_name,label_name,block_id_list,priority,key_route,receive_time,terminate_time from {repr(order_table)}"
        filter.setdefault("type", "0")  # 默认只有非自动任务
        receive_inter=""   # 下发运单区间
        if filter:
            sql_query_all += " where"
            first_flag = True
            for i, j in filter.items():
                # print(i, j)
                if first_flag:
                    first_flag = False
                else:
                    sql_query_all += " and"
                if i == "terminate_time" or i == "create_time" or i == "receive_time":
                    if not j:
                        receive_inter= f" {i} between 0 and {int(time.time())}"
                        sql_query_all += receive_inter
                    else:
                        if isinstance(j[0], str):
                            if len(j[0].split(":")) == 4:
                                date_format = "%Y-%m-%d %H:%M:%S"
                                j0 = datetime.strptime(j[0], date_format)
                                j1 = datetime.strptime(j[1], date_format)
                                j0_s = calendar.timegm(j0.timetuple())
                                j1_s = calendar.timegm(j1.timetuple())
                                receive_inter=f" {i} between {j0_s} and {j1_s}"
                                sql_query_all += receive_inter
                            else:
                                raise Exception(f"time format is not standard, {j}")
                        else:
                            receive_inter=f" {i} between {j[0]} and {j[1]}"
                            sql_query_all += receive_inter
                else:
                    if isinstance(j, str):
                        sql_query_all += f" {i}=={repr(j)}"
                    else:
                        sql_query_all += f" {i} in {repr(j)}"
        sql_query_all += " order by receive_time"
        if amount:
            sql_query_all += f" limit {amount}"

        print("sql:", sql_query_all)
        try:
            cursor.execute(sql_query_all)
            sql3.commit()
        except Exception as e:
            print(e)
            sql3.close()
        # 发单
        # try:
        data = cursor.fetchall()
        data_dict = [dict(row) for row in data]   # order 数据
        # print("orders",data_dict)
        if receive_inter:
            sql_query_robot = f'SELECT DISTINCT vehicle from {repr(order_table)} where {receive_inter}'
            cursor.execute(sql_query_robot)
        else:
            cursor.execute(f'SELECT DISTINCT vehicle from {repr(order_table)}')
        sql3.commit()
        data = cursor.fetchall()
        vehicle_list = [dict(row).get("vehicle") for row in data]
        dispatchable_vehicles=len(vehicle_list)   # 可以接单的机器人数量
        if undispatchable_idle:
            self.undispatchable_ignore(name=[])
            for v in vehicle_list:
                self.dispatchable(v)
        print("vehicles",vehicle_list)
        vehicle_status = {vehicle: 2 for vehicle in vehicle_list}  # 当前各车的状态 0表示running,1表示blockfinished,2表示order_finished或order_stoped,3 表示暂时不接单
        vehicle_order_li= {vehicle:[0,0,-1,0,-1] for vehicle in vehicle_list}  # 下一个下发的运单id,下一个运单索引, 当前动作块索引, 当前正在执行的运单id,当前运单索引
        order_time=[[0 for vehicle in vehicle_list],[0 for vehicle in vehicle_list]]   # 当前各车运单的receive_time, terminate_time
        # order_time[0][0] = data_dict[0]["receive_time"]
        # order_time[1][0] = data_dict[0]["terminate_time"]
        print("vehicle_order_li",vehicle_order_li)
        for i,j in vehicle_order_li.items():
            for k in range(len(data_dict)):
                if data_dict[k]["vehicle"] == i:
                    vehicle_order_li[i][0] = data_dict[k]["id"]
                    vehicle_order_li[i][1] = k
                    vehicle_order_li[i][2] = -1
                    break
            else:
                vehicle_status[i]=3
                vehicle_order_li[i][0]=-1
                dispatchable_vehicles-=1
                self.undispatchable_ignore(name=i)
                print("undispatchable_ignore",i)
        print("vehicle_order_li",vehicle_order_li)

        print("vehicle_status",vehicle_status)
        finished_type=None
        if addblock_type==1:
            finished_type=2
        if addblock_type==2:
            finished_type=1
        if addblock_type==3:
            pass
        start_time=min(order_time[0])
        start_flag=True
        finished_order_count=0
        for ii in range(20000):
            time.sleep(1)
            if finished_order_count>=len(data_dict):
                break
            # 查询运单状态
            finished_flag = False
            tobedispatched_li = []  # 需要下发的车的列表
            if start_flag:
                for v, li in vehicle_order_li.items():
                    if li[0] != -1:
                        tobedispatched_li.append(v)
                start_flag=False
                finished_flag=True
            else:
                finished_vehicle_count=0
                for i,j in vehicle_order_li.items():
                    if j[3]:
                        state = self.getOrderState(f"{i}:{j[3]}")
                        if state == "WAITING":
                            vehicle_status[i] = 1
                            finished_flag = True
                            tobedispatched_li.append(i)
                        elif state == "FINISHED" or state == "STOPPED":
                            vehicle_status[i] = 2
                            if j[0]==-1:
                                if j[1]!=-1:
                                    j[1]=-1
                                    j[3]=None
                                    finished_order_count+=1
                                    dispatchable_vehicles-=1
                                    self.undispatchable_ignore(name=i)
                            else:
                                finished_vehicle_count+=1
                                finished_order_count += 1
                                finished_flag = True
                                tobedispatched_li.append(i)
                if finished_vehicle_count == dispatchable_vehicles:
                    start_time += range_t
                print("tobedispatched_li",tobedispatched_li)
            if finished_flag==False:
                time.sleep(10)
                continue

            print(vehicle_status)
            print("vehicle_order_di",vehicle_order_li)
            # 下发数据库运单
            for vehicle in tobedispatched_li:
                if vehicle_status[vehicle]==1:
                    # add_block
                    block_dt={}
                    # print("block_id_list",data_dict[vehicle_order_li[vehicle][4]]["block_id_list"].split(','))
                    block_id_list=data_dict[vehicle_order_li[vehicle][4]]["block_id_list"].split(',')
                    # print("current_order_index:",vehicle_order_li[vehicle][2])
                    # print("len",len(block_id_list))
                    block_id=data_dict[vehicle_order_li[vehicle][4]]["block_id_list"].split(',')[vehicle_order_li[vehicle][2]+1]
                    cursor.execute(f"select * from Block where id=={repr(block_id)}")
                    sql3.commit()
                    block_data = cursor.fetchall()
                    block_data_dict = [dict(row) for row in block_data]
                    # print(block_data_dict)
                    block_dt.setdefault("id",f"{vehicle}:{vehicle_order_li[vehicle][3]}")
                    block_dt.setdefault("blocks", []).append({})
                    block_dt["blocks"][0].setdefault("blockId",f"{vehicle_order_li[vehicle][3]}:{vehicle_order_li[vehicle][2]+1}")
                    if block_data_dict[0]["location"]:
                        block_dt.get("blocks")[0].setdefault("location",block_data_dict[0]["location"])
                    if block_data_dict[0]['operation']:
                        block_dt.get("blocks")[0].setdefault("operation",block_data_dict[0]["operation"])
                    vehicle_order_li[vehicle][2] += 1  # 当前动作块索引更新
                    complete_flag=True
                    if vehicle_order_li[vehicle][2]+1<len(data_dict[vehicle_order_li[vehicle][4]]["block_id_list"].split(',')):
                        complete_flag=False
                    else:
                        vehicle_order_li[vehicle][2] =-1
                    block_dt.setdefault("complete",complete_flag)
                    # print("block_dt, addblock",vehicle,block_dt)
                    res=requests.post(url=f"{self.ip}/addBlocks",json=block_dt).json()
                    vehicle_status[vehicle]=0
                elif vehicle_status[vehicle]==2:
                    # setOrder
                    if range_t!=-1:
                        if data_dict[vehicle_order_li[vehicle][4]]["receive_time"]-min(order_time[0])>range_t:
                            print("skip")
                            break

                        # if data_dict[vehicle_order_li[vehicle][1]]["receive_time"]-data_dict[vehicle_order_li[vehicle][4]]["receive_time"]>range_t:
                        #     print("skip")
                        #     break
                    order_dt={}
                    vehicle_order_li[vehicle][3] = str(uuid.uuid1())
                    order_dt["id"] = f"{vehicle}:" + vehicle_order_li[vehicle][3]
                    if data_dict[vehicle_order_li[vehicle][1]]["vehicle"]:
                        order_dt.setdefault("vehicle", data_dict[vehicle_order_li[vehicle][1]]["vehicle"])

                    if data_dict[vehicle_order_li[vehicle][1]]["group_name"]:
                        order_dt.setdefault("group", data_dict[vehicle_order_li[vehicle][1]]["group_name"])
                    if data_dict[vehicle_order_li[vehicle][1]]["label_name"]:
                        order_dt.setdefault("label", data_dict[vehicle_order_li[vehicle][1]]["label_name"])
                    if data_dict[vehicle_order_li[vehicle][1]]["priority"]:
                        order_dt.setdefault("priority", data_dict[vehicle_order_li[vehicle][1]]["priority"])
                    if data_dict[vehicle_order_li[vehicle][1]]["key_route"]:
                        order_dt.setdefault("keyRoute", data_dict[vehicle_order_li[vehicle][1]]["key_route"])
                    if addblock_type==1:
                        block_count = 0
                        for block in data_dict[vehicle_order_li[vehicle][1]]['block_id_list'].split(','):
                            cursor.execute(f"select * from Block where id=={repr(block)}")
                            sql3.commit()
                            block_data = cursor.fetchall()
                            block_data_dict = [dict(row) for row in block_data]
                            order_dt.setdefault("blocks", []).append({})
                            if block_data_dict[0]['location']:
                                order_dt.get("blocks")[block_count].setdefault('location',
                                                                               block_data_dict[0]['location'])
                            if block_data_dict[0]['operation']:
                                order_dt.get("blocks")[block_count].setdefault('operation',
                                                                               block_data_dict[0]['operation'])
                            order_dt.get("blocks")[block_count].setdefault('blockId',
                                                                               vehicle_order_li[vehicle][3] + ":" + str(
                                                                                   block_count))
                            block_count += 1
                        order_dt.setdefault("complete", True)
                    elif addblock_type==2: # 追加动作块模式
                        blocks=data_dict[vehicle_order_li[vehicle][1]]['block_id_list'].split(',')
                        current_block=blocks[0]
                        cursor.execute(f"select * from Block where id=={repr(current_block)}")
                        sql3.commit()
                        block_data = cursor.fetchall()
                        block_data_dict = [dict(row) for row in block_data]
                        order_dt.setdefault("blocks", []).append({})
                        if block_data_dict[0]['location']:
                            order_dt.get("blocks")[0].setdefault('location',
                                                                           block_data_dict[0]['location'])
                        if block_data_dict[0]['operation']:
                            order_dt.get("blocks")[0].setdefault('operation',
                                                                           block_data_dict[0]['operation'])
                        order_dt.get("blocks")[0].setdefault('blockId',
                                                                       vehicle_order_li[vehicle][3] + ":0" )
                        if len(blocks)>1:
                            # print("blocks",blocks)
                            order_dt.setdefault("complete", False)
                        else:
                            order_dt.setdefault("complete", True)
                    # todo addblock_type==3
                    # print("order_dt",order_dt)
                    # print("sendorder",vehicle,vehicle_order_li[vehicle][0] ,order_dt["vehicle"],order_dt["id"],order_dt["complete"],len(order_dt["blocks"]))
                    time.sleep(0.5)
                    res_setorder=requests.post(url=f"{self.ip}/setOrder", json=order_dt).json()
                    # 更新索引
                    vehicle_order_li[vehicle][4] = vehicle_order_li[vehicle][1]
                    order_time[0][vehicle_list.index(vehicle)] = data_dict[vehicle_order_li[vehicle][4]]["receive_time"]
                    vehicle_order_li[vehicle][2] = 0
                    for i in range(vehicle_order_li[vehicle][1]+1, len(data_dict)):
                        if data_dict[i]["vehicle"] == vehicle:
                            vehicle_order_li[vehicle][0] = data_dict[i]["id"]
                            vehicle_order_li[vehicle][1] = i
                            break
                    else:
                        vehicle_order_li[vehicle][0] = -1
                    vehicle_status[vehicle]=0




        # except Exception as e:
        #     print("error",e)
        # finally:
        #     sql3.close()
        sql3.close()



    def core_robot_config(self,vehicle_id=None,rotate:bool=True,speed=None,charge:bool=False,goods_shape:str="[-0.64,-0.52,0.64,0.52]",delay:bool=False):
        """core 仿真车一键配置
        :param: rotate 仿真旋转,默认旋转
        :param: charge 充电
        :param: load   载货的货物仿真
        :param: delay  动作延迟(有bug,建议暂不使用) https://seer-group.coding.net/p/robokit/requirements/issues/2239/detail
        :param: speed 速度
        """
        data = {}
        if vehicle_id:
            data.setdefault("vehicle_id", vehicle_id)
        if rotate:
            data.setdefault("disable_rotate",False)
            data.setdefault("rotate_speed",0.3)
        if speed:
            data.setdefault("speed", speed)
        if charge:
            data.setdefault("enable_battery_consumption",True)
            data.setdefault("no_task_battery_consumption",0.05)
            data.setdefault("task_battery_consumption",0.1)
        if goods_shape:
            data.setdefault("load_unload_goods_shape",goods_shape)
        if delay:
            data.setdefault("pause_upon_operation", True)
        requests.post(url=f"{self.ip}/updateSimRobotState",json=data)

    def version(self):
        return str(requests.get(url=f"{self.ip}/version").content)

    def is_on_duty(self):
        """
        获取机器人上/下班状态。
        发送 GET 请求到 /isOnDuty 接口，并返回当前机器人状态。
        Returns: dict: 包含机器人上/下班状态信息的字典。
        """
        # 发送 POST 请求到 /dutyOperations
        try:
            r = requests.get(core.ip + "/isOnDuty")
            if r.status_code == 200:
                return r.json()  # 返回状态数据
            return None
        except Exception:
            return None

    def duty_operations(self, on_duty: bool):
        """ 修改机器人上/下班状态
        Args:
            on_duty (bool): 是否上班，True表示上班，False表示下班
        """
        d = json.dumps({"onDuty": on_duty})
        # 发送 POST 请求到 /dutyOperations
        r = requests.post(self.ip + "/dutyOperations", data=d)
        print(r.json())  # 打印响应内容












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

        # print("*******【" + method + " " + comple_url + " 】*******")

        option = getattr(requests, method, None)
        if not method:
            return
        res = option(comple_url, params=params, json=kwargs, headers=self.header)
        # print("*" * 20 + "【    响应信息   】" + "*" * 20)

        # print("*" * 20 + "【Http 状态码：" + str(res.status_code) + "】" + "*" * 20)

        body = None
        try:
            body = json.dumps(res.json())
            # print(json.dumps(res.json(), indent=4, separators=(",", ":")))
        except:
            pass
        print(f"{method.upper()} {comple_url} {res.status_code} {body}")

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

    def reloc(self,data:dict):
        """机器人重定位
           :param:  data --> {"angle":4.3,"length":0.98,"vehicle":"rbk0","x":-3.9,"y":-5.5}
        """
        self.path="/reloc"
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
    core = OrderLib(getServerAddr())
    print(core.getCoreError())
    errors = core.getCoreError()
    for err in errors:
        if err["code"] == 52107 and "(sim_01: wait for SHT-218)" in err["desc"]:
            assert False
    assert True
    # details = order.orders()
    # print(details.keys())
    # print(len(details["list"]))
    # order.locked()
    # order.gotoOrder(location= "LM314")
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
