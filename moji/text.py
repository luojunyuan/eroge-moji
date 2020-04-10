from qtpy.QtCore import QObject, Signal

from . import utils
from .hook import Hooker

debug = utils.Logger.debug()


class TextManager(QObject):
    __instance = None
    sendTexts = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self._cur_thread = '-1'

        Hooker.instance().onRawTexts.connect(self.text_process)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # XXX maybe not necessary
    @property
    def cur_thread(self):
        return self._cur_thread

    @cur_thread.setter
    def cur_thread(self, value):
        self._cur_thread = value

    def text_process(self, raw_data):
        """获取 Hooker 传来的每一行数据"""
        index = raw_data.index
        code = raw_data.code
        text = raw_data.text

        if index == '-1':
            return
        if self.cur_thread != '-1' and self.cur_thread == index:
            debug('text send emit!')
            TextManagerQMLPlugin.instance.showText.emit(text)

        self.sendTexts.emit(index, code, text)


class TextManagerQMLPlugin(QObject):
    instance = None
    showText = Signal(str)

    def __init__(self):
        super().__init__()
        TextManagerQMLPlugin.instance = self
        debug('TextManagerQMLPlugin is called!')
