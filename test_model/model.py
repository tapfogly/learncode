import paramiko
import json

file_path = "/usr/local/etc/.SeerRobotics/rbk/resources/models/robot.model"


def battery_enable():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="192.168.192.5", port=22, username="sr", password="sr")

        stdin, stdout, stderr = ssh.exec_command(f"cat {file_path}")
        data = json.loads(stdout.read())

        ssh.close()

        device_type = data["deviceTypes"]

        for i in range(len(device_type)):
            if device_type[i]["name"] == "battery":
                param = device_type[i]["devices"]
                for k in range(len(param)):
                    if param[k]["name"] == "battery":
                        if param[k]["isEnabled"]:
                            # print(param[k]["isEnabled"])
                            param[k]["isEnabled"] = False
            elif device_type[i]["name"] == "led":
                param = device_type[i]["devices"]
                for k in range(len(param)):
                    if param[k]["name"] == "led":
                        if param[k]["isEnabled"]:
                            # print(param[k]["isEnabled"])
                            param[k]["isEnabled"] = False

        with open("robot.model", "w") as f:
            f.write(json.dumps(data, separators=(",", ":")))

        tran = paramiko.Transport('192.168.192.5', 22)
        tran.connect(username="sr", password="sr")
        sftp = paramiko.SFTPClient.from_transport(tran)
        local_path = "robot.model"
        remote_path = file_path
        put = sftp.put(local_path, remote_path)
        print(put)
        tran.close()
        print("运行成功")

    except:
        print("请连接")


if __name__ == '__main__':
    while True:
        battery_enable()
