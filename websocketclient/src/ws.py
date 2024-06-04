# from datetime import datetime
import json
import time
from cdps.utils.logger import Log
import websocket

class ws():

    code = int(0)
    log = Log()
    wsc : websocket.WebSocketApp
    ws_send : None
    data_obj_on : None
    ws_server_count = []
    select_count = int(0)
    callback_name : None

    def init(self, ws_send_server):
        ws.ws_send = ws_send_server

    def on_message(ws, message, callback):
        callback(message)


    def on_error(self, error):
        ws.log.logger.info("Error: " + str(error))


    def on_close(self, close_status_code, close_msg):
        ws.log.logger.info(f"Connection closed")
        if ws.code != 999:
            time.sleep(3)
            ws_server_count_num = len(ws.ws_server_count) - 1
            if ws_server_count_num != int(1):
                ws.select_count += int(1)
                if ws.select_count > ws_server_count_num: ws.select_count = int(0)
            ws.start_client(ws, ws.callback_name, ws.ws_server_count, ws.select_count, ws.data_obj_on)


    def close_ws(self, status=int(0)):
        ws.code = status
        if ws.code != 999:
            ws.wsc.close()


    def on_open(self):
        if isinstance(ws.ws_send, dict):
            if not ws.ws_send:
                ws.wsc.send("Hello")
            else:
                ws.wsc.send(json.dumps(ws.ws_send))
        elif isinstance(ws.ws_send, str):
            ws.wsc.send(ws.ws_send)
        else:
            ws.wsc.send("Hello")
        ws.log.logger.info(f"WS open, server = {ws.ws_server_count[ws.select_count]}")


    def start_client(self, callback:None, ws_server:list, select_ws_server:int, data_obj):
        ws.data_obj_on = data_obj
        ws.ws_server_count = ws_server
        ws.select_count = select_ws_server
        ws.callback_name = callback

        websocket.enableTrace(False)
        ws.wsc = websocket.WebSocketApp(ws.ws_server_count[ws.select_count],
                                    on_open=self.on_open,
                                    on_message=lambda ws, msg: self.on_message(
                                        ws, msg, callback),
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        data_obj.init(ws.wsc)
        ws.wsc.run_forever()
