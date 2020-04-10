import logging
import psutil
from psutil import NoSuchProcess, AccessDenied

from qtpy.QtCore import QFileInfo, QObject
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QFileIconProvider

from .libs import win32lib


class Logger(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d in %(funcName)s(): %(message)s')

    @classmethod
    def debug(cls):
        cls()
        logger = logging.getLogger()
        return logger.debug


class Process:
    def __init__(self, pid, name, path, dir_=None, icon=None):
        self.pid = pid
        self.name = name
        self.path = path
        self.dir = dir_
        self.icon = icon


# XXX 建议使用 Findwindow 判断窗口，返回的句柄不为空为打开的
def windows_iter():
    saved_pid = set()
    saved_name = set()
    for pid in win32lib.process_iter():
        if pid in saved_pid:
            continue
        saved_pid.add(pid)
        p = psutil.Process(pid)
        if p.pid and p.is_running():
            try:
                name = p.name()
                if name in saved_name:
                    continue
                saved_name.add(name)
                path = p.cwd()
                dir_ = path[path.rfind('\\') + 1:]
                path = p.exe()
                icon = QIcon(QFileIconProvider().icon(QFileInfo(path)))
            except NoSuchProcess:
                continue
            except AccessDenied:
                continue

            yield Process(p.pid, name, path, dir_, icon)


# FIXME 耗时方法
def find_all_pid(path: str) -> list:
    """通过进程路径获取该进程及其所有子进程 pid

    :param path: Process path
    :return: 某一进程的pid列表
    """
    pid_list = []
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            if p.exe() == path:
                pid_list.append(p.pid)
        except NoSuchProcess:
            continue
        except AccessDenied:
            continue

    return pid_list


def clear_layout(layout, delwidget=False):
    """

    :param layout: QLayout
    :param delwidget: bool
    :return:
    """
    if layout:
        while not layout.isEmpty():
            item = layout.takeAt(0)  # QLayoutItem
            if delwidget:
                widget = item.widget()
                if widget:
                    widget.hide()  # FIXME: memory leak here
                    # del widget
                item_as_layout = item.layout()  # cast item to layout
                if item_as_layout:
                    clear_layout(item_as_layout, delwidget=delwidget)
