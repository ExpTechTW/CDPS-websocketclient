from cdps.plugin.events import Event


class onRun(Event):
    """ 當 伺服器 啟動 """

    def __init__(self):
        self.is_run = False #是否為初次啟動

class onData(Event):
    """ 當 取得 資料 """

    def __init__(self, data:dict):
        self.data = data #取得 資料