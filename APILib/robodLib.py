import json
import socket
import struct
from datetime import datetime, timedelta

PACK_FMT_STR = '!BBHLH6s'


class RobodLib:
    def __init__(self, ip: str):
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, 19208))
        self.sock.settimeout(30)

    def request(self, msgType: int, reqId: int = 1, msg = None,
                sock: socket.socket = None):
        """
        发送请求

        :param msgType: 报文类型
        :param reqId: 序号
        :param msg: 消息体/数据区
        :param sock:  使用指定的socket
        :return: 响应，包含报文头和报文体的元组，报文头[2：序号 3：报文体长度 4：报文类型]
        """
        if sock:
            # 如果指定了socket，则使用指定的socket,否则使用报文类型对应的socket
            so = sock
        else:
            so = self.sock
        ################################################################################################################
        # 打印socket信息
        print("*" * 20, "socket信息", "*" * 20)
        print(f"{'socket:':>10}\tserver{so.getpeername()},local{so.getsockname()}")
        print()
        ################################################################################################################
        # 封装报文
        if msg is not None:
            # 如果报文体不为空，则使用报文体
            if isinstance(msg, (dict, list)):
                # 如果报文体是dict或者list，则转换成字节
                body = bytearray(json.dumps(msg), "ascii")
            else:
                # 如果报文体是bytes或者bytearray，则直接使用
                body = msg
            msgLen = len(body)
        else:
            msgLen = 0
        rawMsg = struct.pack(PACK_FMT_STR, 0x5A, 0x01, reqId, msgLen, msgType, b'\x00\x00\x00\x00\x00\x00')
        ################################################################################################################
        # 打印请求报文信息
        print("*" * 20, "请求信息", "*" * 20)
        print(f"{'时间:':　>6}\t", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), sep='')
        print(f"{'报文类型:':　>6}\t{msgType}\t{msgType:#06X}")
        print(f"{'序号:':　>6}\t{reqId}\t{reqId:#06X}")
        print(f"{'报文头:':　>6}\t{rawMsg.hex(' ').upper()}")
        print(f"{'报文体长度:':　>6}\t{msgLen}\t{msgLen:#010X}")
        if msgLen == 0:
            print(f"{'报文体:':　>6}\t无")
        else:
            print(f"{'报文体:':　>6}\t{body[:1000]}")
            if msgLen > 1000:
                print("...")
        print()
        ################################################################################################################
        # 发送报文
        if msgLen > 0:
            rawMsg += body
        so.send(rawMsg)
        # 接收报文头
        headData = so.recv(16)
        # 解析报文头
        header = struct.unpack(PACK_FMT_STR, headData)
        # 获取报文体长度
        bodyLen = header[3]
        readSize = 1024
        recvData = b''
        while (bodyLen > 0):
            recv = so.recv(readSize)
            recvData += recv
            bodyLen -= len(recv)
            if bodyLen < readSize:
                readSize = bodyLen
        ################################################################################################################
        # 打印响应报文信息
        print("*" * 20, "响应信息", "*" * 20)
        print(f"{'时间:':　>6}\t", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), sep='')
        print(f"{'报文类型:':　>6}\t{header[4]}\t{header[4]:#06X}")
        print(f"{'序号:':　>6}\t{header[2]}\t{header[2]:#06X}")
        print(f"{'报文头:':　>6}\t{headData.hex(' ').upper()}")
        print(f"{'报文体长度:':　>6}\t{header[3]}\t{header[3]:#010X}")
        print(f"{'报文体:':　>6}\t{recvData[:1000]}")
        if header[3] > 1000:
            print("...")
        print()
        ################################################################################################################
        return header, recvData

    def robot_core_shutdown_req(self):
        """
        关闭操作系统
        """
        return self.request(5000)

    def robot_core_reboot_req(self):
        """
        重启操作系统
        """
        return self.request(5003)

    def robot_core_end_req(self):
        """
        关闭 Robokit程序
        """
        return self.request(5001)

    def robot_core_start_req(self):
        """
        启动Robkit程序
        """
        return self.request(5002)

    def robot_core_restart_req(self):
        """
        重新启动 Robokit 程序
        """
        return self.request(5004)

    def robot_core_config_req(self):
        """
        配置robod
        """
        return self.request(5010)

    def robot_core_status_req(self):
        """
        查询rbk状态
        """
        return self.request(5011)

    def robot_core_wifi_req(self, ssid: str, passwd: str = None, nonBroadcast: bool = None):
        """
        连接无线网络\n
        连接无线网络时，如果当前连接的服务器ip是无线网ip，则切换完无线网络后会断开，不会有返回数据，所以建议在连接本地有线ip情况下切换网络，
        切换成功后会返回数据，如果发送的json数据为空，则返回错误码

        :param ssid: SSID名称
        :param passwd: 密码
        :param nonBroadcast: true：隐藏网络 false：广播网络
        """
        d = {"ssid": ssid}
        if passwd:
            d["passwd"] = passwd
        if nonBroadcast:
            d["nonBroadcast"] = nonBroadcast
        return self.request(5020, 1, d)

    def robot_core_set_linux_ssid_ip_req(self, ssid: str, dhcp: bool, ip: str, mask: str, passwd: str = None,
                                         nonBroadcast: bool = None, gateway: str = None):
        """
        连接无线网络\n
        连接无线网络时，如果当前连接的服务器ip是无线网ip，则切换完无线网络后会断开，不会有返回数据，所以建议在连接本地有线ip情况下切换网络，
        切换成功后会返回数据，如果发送的json数据为空，则返回错误码

        :param ssid: SSID名称
        :param dhcp: 是否启用动态获取
        :param ip: 配置的ip
        :param mask: 子网掩码
        :param passwd: 密码
        :param nonBroadcast: true：隐藏网络 false：广播网络
        :param gateway: 配置的网关
        """
        d = {"ssid": ssid, "dhcp": dhcp, "ip": ip, "mask": mask}
        if passwd:
            d["passwd"] = passwd
        if nonBroadcast:
            d["nonBroadcast"] = nonBroadcast
        if gateway:
            d["gateway"] = gateway
        return self.request(5113, 1, d)

    def robot_core_setip_req(self, dhcp: bool, ip: str, mask: str, gateway: str = None):
        """
        配置无线网卡IP\n
        如果当前连接的IP是无线时，配置完会断开，不会有返回数据，所以建议使用网线配置网络

        :param dhcp:
        :param ip:
        :param mask:
        :param gateway:
        """
        d = {"dhcp": dhcp, "ip": ip, "mask": mask}
        if gateway:
            d["gateway"] = gateway
        return self.request(5021, 1, d)

    def robot_core_net_req(self, Mac: str, name: str, dhcp: bool, ip: str, mask: str, gateway: str = None):
        """
        查询当前连接的 Wi-Fi 网络信息\n
        如果当前无线网卡处于关闭状态，则返回数据为空

        :param Mac: MAC地址
        :param name: 网卡描述
        :param dhcp: 是否启用dhcp
        :param ip: 无线网ip
        :param mask: 子网掩码
        :param gateway: 网关
        """
        d = {"Mac": Mac, "name": name, "dhcp": dhcp, "ip": ip, "mask": mask}
        if gateway:
            d["gateway"] = gateway
        return self.request(5022, 1, d)

    def robot_core_wifilist_req(self):
        """
        查询所有可连接 Wi-Fi 列表 (隐藏网络不在其中)
        """
        return self.request(5023)

    def robot_core_hotspot_config_req(self, dhcp: bool, ip: str, mask: str, gateway: str = None):
        """
        配置机器人的热点参数

        :param dhcp: 是否启用动态获取
        :param ip: 配置的ip
        :param mask: 子网掩码
        :param gateway: 配置的网关
        """
        d = {"dhcp": dhcp, "ip": ip, "mask": mask}
        if gateway:
            d["gateway"] = gateway
        return self.request(5031, 1, d)

    def robot_core_hotspot_start_req(self, ssid: str, passwd: str):
        """
        启动机器人热点

        :param ssid: 热点名称
        :param passwd: 热点密码
        """
        return self.request(5032, 1, {"ssid": ssid, "passwd": passwd})

    def robot_core_hotspot_stop_req(self):
        """
        停止机器人热点
        """
        return self.request(5033)

    def robot_core_hotspot_fix_req(self):
        """
        修复机器人热点
        """
        return self.request(5034)

    def robot_core_hotspot_status_req(self):
        """
        查询热点状态
        """
        return self.request(5035)

    def robot_core_robod_version_req(self):
        """
        查询robod版本
        """
        return self.request(5041)

    def robot_core_robod_all1_req(self):
        """
        把 Config.ini 配置的相关所有文件压缩成.zip传输给客户端(子线程运行)
        """
        return self.request(5042)

    def robot_core_robod_id_req(self):
        """
        查询固件id
        """
        return self.request(5043)

    def robot_core_networkcard_req(self, networkCardIndex: int, disabled: bool):
        """
        控制机器人网卡（启用/禁用等）\n
        如果当前连接的是无线网卡ip，禁用网卡之后会断开连接，不会有返回数据,这里的网卡在 Linux 网卡名: eth1

        :param networkCardIndex: 0有线网卡，1无线网卡
        :param disabled: true:禁用网卡 false:启用
        """
        return self.request(5044, 1, {"networkCardIndex": networkCardIndex, "disabled": disabled})

    def robot_core_alxnet_req(self):
        """
        查询有线网卡信息\n
        如果有线网卡已禁用则返回警告提示
        """
        return self.request(5045)

    def robot_core_alxsetip_req(self, name: str, dhcp: bool, ip: str, mask: str, gateway: str = None):
        """
        配置有线网卡网卡 IP

        :param name: 网卡名称
        :param dhcp: 是否启用动态获取
        :param ip: IP
        :param mask: 子网掩码
        :param gateway: 网关
        """
        d = {"name": name, "dhcp": dhcp, "ip": ip, "mask": mask}
        if gateway:
            d["gateway"] = gateway
        return self.request(5046, 1, d)

    def robot_core_audiodriverlist_req(self):
        """
        获取音频驱动列表及音量大小
        """
        return self.request(5047)

    def robot_core_setvolumelevel_req(self, defalutDeviceName: str, volume: int):
        """
        设置音频驱动音量大小

        :param defalutDeviceName: 驱动名称(仅window需要，其他缺省)
        :param volume: 音量大小(0~100)
        """
        return self.request(5048, 1, {"defalutDeviceName": defalutDeviceName, "volume": volume})

    def robot_core_filelist_req(self, path: str):
        """
        查询指定路径下的文件列表

        :param path: 文件路径
        """
        return self.request(5100, 1, {"path": path})

    def robot_core_getfile_req(self, path: str, file_name: str):
        """
        下载指定路径下的文件

        :param path: 文件路径
        :param file_name: 文件名称
        """
        return self.request(5101, 1, {"path": path, "file_name": file_name})

    def robot_core_removefile_req(self, path: str, file_name: str):
        """
        删除指定路径下的文件

        :param path: 文件路径
        :param file_name: 文件名称
        """
        return self.request(5102, 1, {"path": path, "file_name": file_name})

    def robot_core_copyabledirs_req(self):
        """
        查询机器人上可以下载的所有文件夹名称
        """
        return self.request(5103)

    def robot_updaterobokit_cover_req(self, path: str, file_name: str):
        """
        更新RoboKit覆盖

        :param path: 文件路径
        :param file_name: 文件名
        """
        return self.request(5106, 1, {"path": path, "file_name": file_name})

    def robot_updaterobokit_renew_req(self, path: str, file_name: str):
        """
        完全覆盖更新 Robokit

        :param path: 文件路径
        :param file_name: 文件名
        """
        return self.request(5107, 1, {"path": path, "file_name": file_name})

    def robot_core_robod_export_req(self):
        """
        导出Robokit 在Config.ini 配置的所有文件并打包成.zip
        """
        return self.request(5108)

    def robot_core_robod_import_req(self, path: str):
        """
        导入Robokit 在Config.ini 配置的所有文件并打包成.zip

        :param path: zip文件路径
        """
        with open(path, "rb") as f:
            d = f.read()
        return self.request(5109, 1, d)

    def robot_core_uploadfile_req(self, path: str, file_name: str):
        """
        上传配置文件

        :param path: 文件路径
        :param file_name: 文件名
        """
        return self.request(5110, 1, {"path": path, "file_name": file_name})

    def robot_core_reduction_robot_req(self):
        pass

    def robot_core_download_backupfile_req(self):
        pass

    def robot_core_upgrade_robot_req(self):
        pass

    def robot_core_remove_backupfile_req(self):
        pass

    def robot_core_active_robot_req(self):
        pass

    def robot_core_backup_robot_req(self):
        pass

    def robot_core_backup_robotlist_req(self):
        pass

    def robot_core_getrbklogtext_req(self):
        pass

    def robot_core_timingConnectionEthernet_req(self):
        pass

    def robot_core_ntp_timezones_req(self):
        pass

    def robot_core_ntp_setTimezone_req(self):
        pass

    def robot_core_datetime_req(self):
        pass

    def robot_core_iwconfig_req(self):
        pass

    def robot_core_importpxf_req(self):
        pass

    def robot_core_shell_req(self):
        pass

    def robot_core_shell_ping_req(self):
        pass

    def robot_core_disMothod_req(self):
        pass

    def robot_core_robod_import_config_req(self):
        pass

    def robot_core_import_network_req(self):
        pass

    def robot_core_export_network_req(self):
        pass

    def robot_core_get_debug_fileList_req(self,
                                          startTime = datetime.now() - timedelta(minutes=30),
                                          endTime = datetime.now(),
                                          isDownloadLogOnly: bool = False):
        d = {"isDownloadLogOnly": isDownloadLogOnly}
        if isinstance(startTime, datetime):
            d["startTime"] = startTime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            d["startTime"] = startTime
        if isinstance(endTime, datetime):
            d["endTime"] = endTime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            d["endTime"] = endTime
        return self.request(5130, 1, d)


if __name__ == '__main__':
    r = RobodLib("")
    res = r.robot_core_get_debug_fileList_req(datetime(2022, 6, 10), datetime.now())
    print(res)
