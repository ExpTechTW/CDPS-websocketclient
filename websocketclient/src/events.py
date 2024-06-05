from cdps.plugin.events import Event
import websocket

class onRun(Event):
    """ 當 伺服器 啟動 """

    is_run = False

    def __init__(self):
        self.is_run = onRun.is_run #是否為初次啟動

class onData(Event):
    """ 當 取得 資料 """

    get_data = {}
    get_ws: websocket.WebSocketApp

    def init(self, ws: websocket.WebSocketApp):
        onData.get_ws = ws

    def wirite(self, data: dict):
        onData.get_data = data  # 取得資料

    def get(self):
        return onData.get_data

    def send(self, msg: str):
        if msg != "":
            try:
                onData.get_ws.send(msg)
                return f"{msg} 已發送"
            except websocket.WebSocketConnectionClosedException as e:
                return "WebSocket 連線未建立或已關閉。"
            except Exception as e:
                return f"發生錯誤: {e}"
        return msg