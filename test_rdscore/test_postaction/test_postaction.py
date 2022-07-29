import socketserver
import threading
from pathlib import Path
import sys
print(Path(__file__).absolute().parents[2])
sys.path.append(Path(__file__).absolute().parents[2])
sys.path.append("../..")
from APILib.orderLib import *
import http.server

core = OrderLib(getServerAddr())


def module_setup():
    core.uploadScene(Path(Path(__file__).absolute().parent, "scene.zip"))
    # todo core.clearOldOrders()
    core.modifyParam({"RDSDispatcher": {"ClearDBOnStart": True}})
    time.sleep(5)


# def test_postaction_before_mark_complete():
#     s = requests.session()
#     order_id = str(uuid.uuid1())
#     order = {
#         "id":order_id,
#         "blocks":[{"blockId":order_id+"_block1", "location":"AP23", "postAction":{"configId":"Foxconunload"}}],
#         "complete":False,
#         "vehicle":"sim_01"
#     }
#     s.post(core.ip+'/setOrder', data=json.dumps(order))
#     time.sleep(5)

#     while core.orderDetails(order_id)['state'] != "WAITING":
#         time.sleep(2)


#     core.markComplete(order_id)


def test_postaction_block_suspended():
    s = requests.session()
    order_id = str(uuid.uuid1())
    order = {
        "id": order_id,
        "blocks": [{"blockId": order_id + "_b1", "location": "LM39", }],
        "complete": False,
        "vehicle": "sim_01"
    }
    s.post(core.ip + '/setOrder', data=json.dumps(order))
    time.sleep(5)
    while core.orderDetails(order_id)['state'] != "WAITING":
        time.sleep(2)

    add_blocks = {
        "id": order_id,
        "blocks": [{"blockId": order_id + "_b2", "location": "AP27", "postAction": {"config": "Foxconunload"}}]
    }
    s.post(core.ip + "/addBlocks", data=json.dumps(add_blocks))
    core.markComplete(order_id)

    while core.orderDetails(order_id)['state'] != "FINISHED":
        core.gotoSitePause([])
        core.gotoSiteResume([])


recv_log =[]

class RequestHandler200(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        print(self.headers)
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        print(message)
        self.send_response(code=200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(message), "utf-8"))


def test_postaction_simple_order():
    server = http.server.ThreadingHTTPServer(("", 12321), RequestHandler200)
    try:
        with server:
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            time.sleep(5)
            # todo 上传模型文件
            s = requests.session()
            order_id = str(uuid.uuid1())
            simple_order= {
                "id":order_id,
                "fromLoc":"WS-1-5",
                "toLoc":"WS-1-6",
                "loadPostAction":{"configId":"TestLoad"},
                "unloadPostAction":{"configId":"TestUnload"},
            }
            s.post(core.ip+"/setOrder", json=simple_order)

            core.waitForOrderFinish(order_id)
            print(recv_log)
            # todo expected body
            # todo assert 如何判断收到了回复？

    except Exception as e:
        assert False, "except: {}".format(str(e))


if __name__ == '__main__':
    postaction_simple_order()