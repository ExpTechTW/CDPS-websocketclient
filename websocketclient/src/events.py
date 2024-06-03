from cdps.plugin.events import Event


class onRun(Event):
    """ 當 伺服器 啟動 """

    def __init__(self):
        self.is_run = False #是否為初次啟動
