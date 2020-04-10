from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import QApplication, QMainWindow
from PySide.QtDeclarative import QDeclarativeView

from .ui.process_select import ProcessSelectPage
from .ui.text_select import TextPrefDialog
from .ui.tray import TrayIcon
from .qmlregister import register_qml_type
from .utils import Logger


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.process_page = ProcessSelectPage(self)
        self.setCentralWidget(self.process_page)
        self.text = TextPrefDialog(self)
        self.view = QDeclarativeView()
        self.tray = TrayIcon(self)
        self.tray.show()

        self._connect()

    def _connect(self):
        self.text.textSelected.connect(self.text_display)

    def open_filter(self):
        self.text.set_active(True)
        self.text.show()

    @Slot()
    def text_display(self):
        # FIXME Qrc path is only suit for qml file not dll
        self.view.engine().addImportPath(':/moji/ui/imports')
        self.view.engine().addImportPath('libs/imports')

        self.view.setSource('qrc:main.qml')
        self.view.setAttribute(Qt.WA_TranslucentBackground)
        self.view.setStyleSheet("background-color:transparent")
        self.view.setWindowFlags(Qt.SplashScreen |
                                 Qt.FramelessWindowHint |
                                 Qt.WindowStaysOnTopHint)
        self.view.showFullScreen()


def moji() -> int:
    """entry point"""
    app = QApplication([])

    register_qml_type()

    win = MainWindow()
    win.show()

    return app.exec_()
