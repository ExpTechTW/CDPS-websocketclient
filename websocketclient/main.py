import datetime
import json
import threading
from cdps.plugin.manager import Manager, Listener
from cdps.plugin.events import Event,onServerStartEvent
from cdps.utils.logger import Log

import plugins.websocketclient.src.ws as ws_
from plugins.websocketclient.src.events import onRun

###

with open("./config/websocketclient.json", 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

# class onServerStartListener(Listener):
#     event = onServerStartEvent
#     is_run = False

#     def on_event(self, event):
#         if (self.is_run == False):
#             ws_.init(config['ws_send_server'])
#             task_thread_1 = threading.Thread(target=self.get_websocket)
#             task_thread_1.start()
#             self.is_run = True

def data_store(new_data):
    lastest_time = datetime.datetime.now()
    try:
        new_data = json.loads(new_data)
    except:
        pass
    if type(new_data) == dict:
        log.logger.info(new_data)
        if new_data["type"] == "data":
            log.logger.info(new_data)

def ws_callback(message):
    data_store(message)

def get_websocket(stop_event):
    while not stop_event.is_set():
        ws_.start_client(ws_callback, config['ws_server'], config['select_ws_server'])

def task(stop_event):
    event_manager.call_event(onRun())
    if (onRun().is_run == False):
        ws_.init(config['ws_send_server'])
        task_thread_1 = threading.Thread(target=get_websocket, args=(stop_event,))
        task_thread_1.start()
        onRun().is_run = True

log = Log()
event_manager = Manager()
# event_manager.register_listener(onServerStartListener())

###

# class onServerStartEventForExampleEvent(Event):
#     """ 當 伺服器 啟動 """
#     def __init__(self, pid):
#         self.pid = pid

# original_on_start = cdps.cdps_server.CDPS.on_start

# def _new_on_start(self):
#     self.event_manager.call_event(onServerStartEventForExampleEvent("example"))
#     original_on_start(self)

# cdps.cdps_server.CDPS.on_start = _new_on_start

# class onServerStartEventForExampleListener(Listener):
#     event = onServerStartEventForExampleEvent
#     is_run = False

#     def on_event(self, event):
#         if (self.is_run == False):
#             print("holle word!")
#             print(event.pid)
#             print("2!")
#             self.is_run = True

# event_manager.register_listener(onServerStartEventForExampleListener())