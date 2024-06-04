# from datetime import datetime
import json
import time
from cdps.utils.logger import Log
import websocket

code = int(0)
log = Log()
ws = None

def init(ws_send_server):
    global ws_send
    ws_send = ws_send_server

def on_message(ws, message, callback):
    callback(message)


def on_error(ws, error):
    log.logger.info("Error: " + str(error))


def on_close(ws, close_status_code, close_msg):
    log.logger.info(f"Connection closed")
    if code != 999:
        time.sleep(3)
        ws_server_count_num = len(ws_server_count)
        if ws_server_count_num != int(1):
            select_count += int(1)
            if select_count > ws_server_count_num: select_count = int(0)
        ws.close()
        start_client(callback_name, ws_server_count, select_count, data_obj_on)


def close_ws(ws, status=int(0)):
    global code
    code = status
    if code != 999:
        ws.close()


def on_open(ws):
    if isinstance(ws_send, dict):
        if not ws_send:
            ws.send("Hello")
        else:
            ws.send(json.dumps(ws_send))
    elif isinstance(ws_send, str):
        ws.send(ws_send)
    else:
        ws.send("Hello")
    log.logger.info(f"WS open, server = {select_count}")


def start_client(callback:None, ws_server:list, select_ws_server:int, data_obj):
    global ws, callback_name, select_count, ws_server_count, data_obj_on
    data_obj_on = data_obj
    ws_server_count = ws_server
    select_count = select_ws_server
    callback_name = callback

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(ws_server_count[select_count],
                                on_open=on_open,
                                on_message=lambda ws, msg: on_message(
                                    ws, msg, callback),
                                on_error=on_error,
                                on_close=on_close)

    data_obj.init(ws)
    ws.run_forever()
