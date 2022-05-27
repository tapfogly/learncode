import socket
import json
import time
import struct
import math

PACK_FMT_STR = '!BBHLH6s'
def getIP()->str:
    """获取机器人ip

    Returns:
        str: ip
    """
    with open("config.json", "r") as f:
        j = json.load(f)
        return j.get("rbk_ip","")

def packMasg(reqId, msgType, msg={}):
    msgLen = 0
    jsonStr = ""
    if isinstance(msg, dict):
        jsonStr = json.dumps(msg)
    else:
        jsonStr = msg
    if (msg != {}):
        msgLen = len(jsonStr)
    print(msgLen,"***************************")
    rawMsg = struct.pack(PACK_FMT_STR, 0x5A, 0x01, reqId, msgLen,msgType, b'\x00\x00\x00\x00\x00\x00')
    # print("{:02X} {:02X} {:04X} {:08X} {:04X}"
    # .format(0x5A, 0x01, reqId, msgLen, msgType))

    if (msg != {}):
        rawMsg += bytearray(jsonStr,'ascii')
        # print(msg)

    return rawMsg
    
def normalize_theta(theta):
    if theta >= -math.pi and theta < math.pi:
        return theta
    multiplier = math.floor(theta / (2 * math.pi))
    theta = theta - multiplier * 2 * math.pi
    if theta >= math.pi:
        theta = theta - 2 * math.pi
    if theta < -math.pi:
        theta = theta + 2 * math.pi
    return theta
class rbklib:
    def __init__(self, ip) -> None:
        self.ip = ip
        self.so_19204 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so_19204.connect((self.ip, 19204))
        self.so_19204.settimeout(5)

        self.so_19205 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so_19205.connect((self.ip, 19205))
        self.so_19205.settimeout(5)

        self.so_19206 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so_19206.connect((self.ip, 19206))
        self.so_19206.settimeout(5)

        self.so_19207 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so_19207.connect((self.ip, 19207))
        self.so_19207.settimeout(5)

    def query(self, msg):
        so = self.so_19204
        so.send(msg)
        dataall = b''

        try:
            data = so.recv(16)
        except socket.timeout:
            print('timeout')
        jsonDataLen = 0
        backReqNum = 0
        if(len(data) < 16):
            print('pack head error')
            print(data)
        else:
            header = struct.unpack(PACK_FMT_STR, data)
            # print("{:02X} {:02X} {:04X} {:08X} {:04X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}       length: {}"
            # .format(header[0], header[1], header[2], header[3], header[4],
            # header[5][0], header[5][1], header[5][2], header[5][3], header[5][4], header[5][5],
            # header[3]))
            jsonDataLen = header[3]
            backReqNum = header[4]
        dataall += data
        data = b''
        readSize = 1024
        jdata = dict()
        try:
            while (jsonDataLen > 0):
                recv = so.recv(readSize)
                data += recv
                jsonDataLen -= len(recv)
                if jsonDataLen < readSize:
                    readSize = jsonDataLen
            jdata = json.loads(data)
        except socket.timeout:
            print('timeout')
        return jdata

    def getResponse(self, so:socket.socket):
        dataall = b''
        try:
            data = so.recv(16)
        except socket.timeout:
            print('timeout')
        jsonDataLen = 0
        backReqNum = 0
        if(len(data) < 16):
            print('pack head error')
            print(data)
        else:
            header = struct.unpack(PACK_FMT_STR, data)
            print("{:02X} {:02X} {:04X} {:08X} {:04X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}       length: {}"
            .format(header[0], header[1], header[2], header[3], header[4],
            header[5][0], header[5][1], header[5][2], header[5][3], header[5][4], header[5][5],
            header[3]))
            jsonDataLen = header[3]
            backReqNum = header[4]
        dataall += data
        data = b''
        readSize = 1024
        try:
            while (jsonDataLen > 0):
                recv = so.recv(readSize)
                data += recv
                jsonDataLen -= len(recv)
                if jsonDataLen < readSize:
                    readSize = jsonDataLen
            print(json.dumps(json.loads(data), indent=1))
            dataall += data
            print(' '.join('{:02X}'.format(x) for x in dataall))
        except socket.timeout:
            print('timeout')

    def reloc(self, pos):
        so = self.so_19205
        print("pos:", pos)
        data = {"x":pos["x"], "y":pos["y"], "angle":pos["angle"]/180.0*math.pi}
        msg = packMasg(1,2002, data)
        so.send(msg)
        self.getResponse(so)

    def confirmLoc(self):
        so = self.so_19205
        msg = packMasg(1,2003)
        so.send(msg)

    def cancelLoc(self):
        so = self.so_19205
        msg = packMasg(1,2004)
        so.send(msg)

    def moveLoc(self, pos):
        # 将agv重定位，并且确认定位
        self.reloc(pos)
        time.sleep(1)
        self.cancelLoc()
        time.sleep(1)
        self.confirmLoc()
    
    def moveRobot(self, pos:dict):
        sim_pos ={"sim":{"setPos":pos}}
        self.sendTask(sim_pos)
        self.reloc(pos = pos)
        time.sleep(1)
        self.cancelLoc()
        time.sleep(1)
        self.confirmLoc()


    def lock(self):
        so = self.so_19207
        data = {"nick_name":"rbklib"}
        msg = packMasg(1,4005, data)
        so.send(msg)

    def uploadMap(self, map_name:str):
        so = self.so_19207
        with open(map_name, 'r') as fid:
            data = fid.read()
            msg = packMasg(1,4010, json.loads(data))
            so.send(msg)
            r.getResponse(so)

    def downMap(self, map_name):
        so = self.so_19207
        data = {"map_name":map_name}
        msg = packMasg(2,4010, data)
        so.send(msg)
        r.getResponse(so)

    def clearErrors(self):
        so = self.so_19207
        msg = packMasg(1,4009)
        so.send(msg)

    def cancelTask(self):
        so = self.so_19206
        msg = packMasg(1,3003)
        so.send(msg)

    def getPos(self):
        pos_msg = packMasg(1,1004)
        data = self.query(pos_msg)
        return data

    def getVel(self):
        pos_msg = packMasg(1,1005)
        data = self.query(pos_msg)
        return data

    def getTaskStatus(self):
        msg = packMasg(1,1020)
        data = self.query(msg)
        return data

    def getRobotStatus(self):
        msg = packMasg(1,1000)
        data = self.query(msg)
        return data

    def getError(self):
        msg = packMasg(1,1050)
        data = self.query(msg)
        return data        

    def getStatusInfo(self):
        msg = packMasg(1, 1000)
        data = self.query(msg)
        return data
        
    def sendTask(self, data):
        so = self.so_19206
        msg = packMasg(1,3051,data)
        so.send(msg)

    def sendTaskList(self, data):
        so = self.so_19206
        task = {"move_task_list": data}
        print(task)
        msg = packMasg(1,3066,task)
        so.send(msg)
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
        so = self.so_19207
        msg = packMasg(1,4101, data)
        so.send(msg)        

    def translate(self, data):
        """机器人平动"""
        so = self.so_19206
        msg = packMasg(1,3055,data)
        so.send(msg)

if __name__ == "__main__":
    # print(getIP())
    r = rbklib(ip = "192.168.133.132")
    r.lock()
    data = {"RBKSim":{"RBKSimMinVx":0.5}}
    r.modifyParam(data = data)
    # pos = {"x":-0.525, "y":-0.06, "angle":0}
    # r.moveRobot(pos=pos)
    # time.sleep(1.0)
    # ts = r.getTaskStatus()
    # while ts is 2:
    #     ts = r.getTaskStatus()
    #     time.sleep(1)
    # if ts["task_status"] == 4:
    #     print("success! stauts = ", ts["task_status"])
    # else:
    #     print("failed! stauts = ", ts["task_status"])
