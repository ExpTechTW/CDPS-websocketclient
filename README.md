# CDPS-websocketclient
<img alt="Discord" src="https://img.shields.io/discord/926545182407688273">

------

## 索引
  - [設定](#設定)
  - [貢獻者](#貢獻者)
  - [發佈規則](#發佈規則)
  - [合作](#合作)

## 設定
- `ws_server` 向伺服器連線的網址
- `select_ws_server` 首次"向伺服器連線的網址"的位置
- `ws_send_server` 向伺服器傳送的訊息
- `log_show` 是否打印伺服器接收的訊息

## 外部擴充示範用法
```py
from cdps.plugin.manager import Manager, Listener
from cdps.plugin.thread import new_thread
from cdps.utils.logger import Log
from cdps.plugin.events import Event
from plugins.websocketclient.src.events import onData
import cdps.cdps_server

class onWsEvent(Event):
    """ 當 伺服器 啟動 """
    def __init__(self, pid):
        self.pid = pid

original_on_start = cdps.cdps_server.CDPS.on_start

def _new_on_start(self):
    self.event_manager.call_event(onWsEvent("test"))
    original_on_start(self)

cdps.cdps_server.CDPS.on_start = _new_on_start

class onWsListener(Listener):
    event = onWsEvent

    def on_event(self, event):
        get_websocket_test()

log = Log()
data_obj = onData()

@new_thread
def get_websocket_test():
    data_get = {}
    while True:
        data_get_temp = data_obj.get()
        if data_get != data_get_temp:
            data_get = data_get_temp
            log.logger.info(f"test {data_get}")

event_manager = Manager()
event_manager.register_listener(onWsListener())
```

## 貢獻者
- yayacat `程式開發` `文檔`

------

## 發佈規則
- 如果新版本中有錯誤，且尚未列出，請將錯誤資訊提交到 ```issue```
- 如果您使用任何形式的辱罵性或貶義性語言給其他用戶，您將永遠被封禁！
- 不要發送重複無意義內容至 ```issue```，否則您將永遠被封禁！
- 若有任何問題或建議，歡迎提出

## 合作
- 若有任何可以改進的地方，歡迎使用 ```Pull requests``` 來提交
