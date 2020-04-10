from qtpy.QtCore import QCoreApplication
from qtpy.QtWidgets import QMenu, QSystemTrayIcon
from PySide.QtGui import QIcon


class TrayIcon(QSystemTrayIcon):
    __instance = None

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self._menu = QMenu(self.parent)

        # self._init_action()
        self._init_ui()
        TrayIcon.__instance = self

    # def _init_action(self):
    #     self.quitAction

    def _init_ui(self):
        self.setIcon(QIcon(':heart.svg'))
        self.setToolTip(QCoreApplication.instance().applicationName())
        self._menu.addAction(self.tr("Quit")).triggered.connect(self.parent.close)

        self.setContextMenu(self._menu)
