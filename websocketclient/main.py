import json
import shutil
from cdps.plugin.manager import Manager, Listener, event_listener
from cdps.plugin.events import onCommandEvent
from cdps.plugin.thread import new_thread
from cdps.utils.logger import Log

from plugins.websocketclient.src.ws import ws
from plugins.websocketclient.src.events import onData, onRun

###

def data_store(new_data):
    try:
        new_msg = json.loads(new_data)
    except:
        pass
    if type(new_msg) == dict:
        data_obj.wirite(new_msg)
        if config['log_show']:
            log.logger.info(data_obj.get())

def ws_callback(message):
    data_store(message)

@new_thread("get_websocket")
def get_websocket():
    if run_obj.is_run == False:
        run_obj.is_run = True
        ws.init(ws, config['ws_send_server'])
        ws.start_client(ws, ws_callback, config['ws_server'], int(config['select_ws_server']), data_obj)

# @new_thread
# def close_test():
#     while True:
#         time.sleep(5)
#         ws.close_ws(ws)
#         time.sleep(5)

# @event_listener(onServerStartEvent)
# class onServerStartListener(Listener):

#     def on_event(self, event):
#         print(event.pid)

# @event_listener(onPluginReloadEvent, "websocketclient")
# class onPluginReloadEventListener(Listener):
#     def on_event(self, event):
#         log.logger.info(event.name)
#         if event.name == "websocketclient":
#             event_manager.unregister_listener(onPluginReloadEventListener(), "websocketclient")
#             ws.close_ws(ws, 999)

@event_listener(onCommandEvent)
class onServerCommandListener(Listener):

    def on_event(self, event):
        if event.command == "wsc close":
            if run_obj.is_run == True:
                ws.close_ws(ws, 999)
                run_obj.is_run = False
            elif run_obj.is_run == False:
                log.logger.warning("websocketclient 的 websocket 已關閉")
        elif event.command == "wsc start":
            if run_obj.is_run == False:
                get_websocket()
            elif run_obj.is_run == True:
                log.logger.warning("websocketclient 的 websocket 已運行")

log = Log()
event_manager = Manager()
run_obj = onRun()
data_obj = onData()
event_manager.call_event(run_obj)
event_manager.call_event(data_obj)

src_file = "./plugins/websocketclient/config.json"
dst_file = "./config/websocketclient.json"
backup_file = "./config/websocketclient_backup.json"
config = {}

with open(dst_file, 'r', encoding='utf-8') as f:
    config:dict = json.loads(f.read())

def copy_config_json():
    global config
    try:
        shutil.copy2(dst_file, backup_file)
        log.logger.info(f"舊設定檔案已成功複製到 {backup_file}")
        # 複製檔案
        shutil.copy2(src_file, dst_file)
        log.logger.info(f"新的設定檔案已成功複製到 {dst_file}")
        with open(dst_file, 'r', encoding='utf-8') as f:
            config = json.loads(f.read())
    except IOError as e:
        log.logger.error(f"無法複製檔案: {e}")
    except Exception as e:
        log.logger.error(f"發生錯誤: {e}")

if 'log_show' not in config:
    copy_config_json()
if config['ws_send_server'] == {}:
    copy_config_json()
if config['log_show']:
    copy_config_json()

get_websocket()

# close_test()