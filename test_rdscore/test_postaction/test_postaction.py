from pathlib import Path
import sys
sys.path.append(Path(__file__).absolute().parents[2])

from APILib.orderLib import *

core = OrderLib(getServerAddr())

def module_setup():
    core.uploadScene(Path(Path(__file__).absolute().parent,"scene.zip" ))
    # todo core.clearOldOrders()
    core.modifyParam({"RDSDispatcher":{"ClearDBOnStart":True}})
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
        "id":order_id,
        "blocks":[{"blockId":order_id+"_b1", "location":"LM39", }],
        "complete":False,
        "vehicle":"sim_01"
    }
    s.post(core.ip+'/setOrder', data=json.dumps(order))
    time.sleep(5)
    while core.orderDetails(order_id)['state'] != "WAITING":
        time.sleep(2)
    
    add_blocks = {
        "id":order_id,
        "blocks":[{"blockId":order_id+"_b2", "location":"AP27","postAction":{"config":"Foxconunload"}}]
    }
    s.post(core.ip+"/addBlocks", data=json.dumps(add_blocks))
    core.markComplete(order_id)

    while core.orderDetails(order_id)['state'] != "FINISHED":
        core.gotoSitePause([])
        core.gotoSiteResume([])
