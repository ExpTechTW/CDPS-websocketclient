import datetime
import json
import shutil
from cdps.plugin.manager import Manager, Listener
from cdps.plugin.events import Event,onServerStartEvent
from cdps.plugin.thread import new_thread
from cdps.utils.logger import Log

import plugins.websocketclient.src.ws as ws_
from plugins.websocketclient.src.events import onData, onRun

###

def data_store(new_data):
    try:
        new_data = json.loads(new_data)
    except:
        pass
    if type(new_data) == dict:
        event_manager.call_event(onData())
        onData().init(new_data)
        if config['log_show']:
            log.logger.info(onData().get())

def ws_callback(message):
    data_store(message)

@new_thread
def get_websocket():
    event_manager.call_event(onRun())
    if (onRun().is_run == False):
        ws_.init(config['ws_send_server'])
        ws_.start_client(ws_callback, config['ws_server'], config['select_ws_server'])
        onRun().is_run = True


log = Log()
event_manager = Manager()

src_file = "./plugins/websocketclient/config.json"
dst_file = "./config/websocketclient.json"
backup_file = "./config/websocketclient_backup.json"

with open(dst_file, 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

if 'log_show' not in config:
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

get_websocket()