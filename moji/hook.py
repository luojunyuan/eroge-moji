from subprocess import Popen, PIPE
from threading import Thread

from qtpy.QtCore import Signal, QObject

CRLF = '\r\n'
PATH = '.\\libs\\textractor\\TextractorCLI.exe'


class TextObject:
    def __init__(self, line: str):
        self.index = '-1'
        self.code = ''
        self.text = ''

        self.__data_cleansing(line.replace('\n', ''))

    def __data_cleansing(self, line: str):
        line = line.split('] ')

        handle = line[0].replace('[', '')
        self.text = line[-1]

        l = handle.split(':')
        self.index = index = l[0]
        try:
            self.code = ('/' + l[6] + ':' + l[7]) if index != '0' and index != '1' else l[5]
        except IndexError:
            self.index = '-1'
            self.code = ''
            self.text = ''


# TODO 也许应该再增加一个判断打开的cli 报错退出失效的逻辑
class Hooker(QObject, Thread):
    """生成一个Textractor脚手架进程

    可以根据pid附加入单个进程，或脱离单个进程，或指定hcode或rcode注入某一进程
    """
    __instance = None
    onRawTexts = Signal(TextObject)

    def __init__(self):
        QObject.__init__(self)
        Thread.__init__(self)

        self.cli = Popen(PATH, encoding='utf-16-le',
                         stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.setDaemon(True)
        self.start()

        Hooker.__instance = self

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def run(self):
        """Start send raw text data"""
        while self.cli.poll() is None:
            try:
                line = self.cli.stdout.readline()
            except UnicodeDecodeError:
                continue

            data = TextObject(line)
            self.onRawTexts.emit(data)

    def attach(self, pid: int) -> None:
        self.cli.stdin.write('attach -P' + str(pid) + CRLF)
        self.cli.stdin.flush()

    def detach(self, pid: int) -> None:
        self.cli.stdin.write('detach -P' + str(pid) + CRLF)
        self.cli.stdin.flush()

    def inject(self, pid: int, hookcode: str) -> None:
        """Must called after attach()"""
        self.cli.stdin.write(hookcode + ' -P' + str(pid) + CRLF)
        self.cli.stdin.flush()
