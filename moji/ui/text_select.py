from functools import lru_cache

from qtpy.QtCore import *
from qtpy.QtGui import QTextCursor
from qtpy.QtWidgets import *

from .. import utils
from ..text import TextManager

debug = utils.Logger.debug()

TEXT_COLUMN_COUNT = 2
TEXT_MAX_HEIGHT = 80
TEXT_MIN_WIDTH = 400


class TextThreadView(QWidget):
    """View of one thread"""

    SELECT_BUTTON_ROW = 0
    CODE_LABEL_ROW = 1

    def __init__(self, index, code, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.code = code
        self.index = index

        self._init_ui()
        self._connect()

    def _init_ui(self):
        layout = QVBoxLayout()

        self.choose_button = QPushButton("选择")
        code_label = QLabel(self.code)

        self.textEdit = QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setMaximumHeight(TEXT_MAX_HEIGHT)
        self.textEdit.setMinimumWidth(TEXT_MIN_WIDTH)

        header = QHBoxLayout()
        header.addWidget(self.choose_button)
        header.addStretch()
        header.addWidget(code_label)

        layout.addLayout(header)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

    def _connect(self):
        self.choose_button.clicked.connect(self.notify_selected)
        # self.parent.textSelected.connect(self.index_check)

    @Slot()
    def notify_selected(self):
        debug(f'text No.{self.index} is selected')
        self.parent.textSelected.emit(self.index)
        TextManager.instance().cur_thread = self.index

    def set_text(self, text):
        self.textEdit.setPlainText(text)
        self.textEdit.moveCursor(QTextCursor.End)

    def append_text(self, text):
        self.textEdit.appendPlainText(text)
        self.textEdit.moveCursor(QTextCursor.End)

    def has_text(self):
        return bool(self.textEdit.toPlainText())


class TextTable(QWidget):
    sizeChanged = Signal()
    message = Signal(str)
    textSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._active = False
        self._text_thread_view = {}  # {index: TextThreadView}

        self._init_ui()

    def _init_ui(self):
        # text thread select area
        text_area = QScrollArea()
        _ = QWidget()
        _.setLayout(self._thread_layout())
        text_area.setWidget(_)
        text_area.setWidgetResizable(True)

        text_group = QGroupBox()
        text_group.setTitle(self.tr("Text threads"))
        _ = QHBoxLayout()
        _.addWidget(text_area)
        text_group.setLayout(_)

        function = QGroupBox(self.tr("Function"))
        function.setMinimumHeight(200)  # hard coded
        function_layout = QVBoxLayout()

        # TODO implement these
        # function_layout.addWidget(self.code_input)
        # function_layout.addWidget(self.regexp_input)
        # function_layout.addWidget(self.text_search)
        function.setLayout(function_layout)

        layout = QVBoxLayout()
        layout.addWidget(function)
        layout.addWidget(text_group)

        self.setLayout(layout)

    @lru_cache(None)
    def _thread_layout(self):
        return QGridLayout()

    def set_active(self, active):
        if self._active != active:
            if active:
                TextManager.instance().sendTexts.connect(self._add_text)
            else:
                TextManager.instance().sendTexts.disconnect(self._add_text)
            self._active = active

    def clear(self):
        # 先判断grid建立没有
        if self._text_thread_view:
            # clear dict
            self._text_thread_view.clear()
            utils.clear_layout(self._thread_layout(), delwidget=True)

    def _update_thread(self, index: str, code, text):
        try:
            view = self._text_thread_view[index]
        except KeyError:
            QTimer().singleShot(0, self.sizeChanged.emit)
            view = TextThreadView(index, code, self)
            self._text_thread_view[index] = view

            n = self._thread_layout().count()
            row = n / TEXT_COLUMN_COUNT
            col = n % TEXT_COLUMN_COUNT
            self._thread_layout().addWidget(view, row, col)

        # view.set_text(text)

    def _add_text(self, index, code, text):
        """获得 TextManager 中 text_process() 传来的每一行数据

        :param index: The sequence of the text
        :param code: hook code made by Textractor
        :param text: game text or console text
        :return:
        """

        view = self._text_thread_view.get(index)
        if not view:
            """新出现的文本线程"""
            self._update_thread(index, code, text)
            view = self._text_thread_view[index]

        if view.has_text():
            view.append_text('\n' + text)
        else:
            view.set_text(text)

    # scenarioThreadChanged = Signal(long, unicode, unicode)  # signature, name, encoding

    # override
    def sizeHint(self):
        n = self._thread_layout().count()
        width = 500
        height = 195  # + 20*2 for 2 msg labels
        if n <= 0:
            pass
        elif n < TEXT_COLUMN_COUNT:
            height += 120 * 2  # XXX 手动控制控件大小
        else:
            row = 1 + (n - 1) / TEXT_COLUMN_COUNT
            height += 125 * (1 + min(row, 3.5))  # max row count is 3
            width += -290 + 350 * TEXT_COLUMN_COUNT
            if row > 2:
                width += 20
        return QSize(width, height)


class TextPrefDialog(QMainWindow):
    textSelected = Signal(str)

    def __init__(self, parent=None):
        flags = Qt.Dialog | Qt.WindowMinMaxButtonsHint
        super().__init__(parent, flags)
        self.setWindowTitle(self.tr("Text Settings"))

        self.text_table = TextTable()
        self.setCentralWidget(self.text_table)

        self._connect()

    def _connect(self):
        self.text_table.message.connect(self.show_message)
        self.text_table.sizeChanged.connect(self.update_size)
        self.text_table.textSelected.connect(self.textSelected)
        self.text_table.textSelected.connect(self.hide)

    def clear(self):
        self.text_table.clear()

    def set_active(self, value):
        self.text_table.set_active(value)

    def show_message(self, text):
        bar = self.statusBar()
        bar.showMessage(text)

    def update_size(self):
        size = self.sizeHint()
        self.setMinimumSize(size)
        self.resize(size)

    # override
    def setVisible(self, visible):
        if visible:
            """set windows icon and title from GameProfile"""
            pass

        if visible != self.isVisible():
            if visible:
                self.clear()
                QTimer().singleShot(0, self.update_size)

        self.set_active(visible)
        super().setVisible(visible)

    # override
    def sizeHint(self):
        return self.centralWidget().sizeHint()
