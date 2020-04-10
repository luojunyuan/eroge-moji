from qtpy.QtCore import QObject, Slot, Qt
from qtpy.QtGui import QStandardItemModel
from qtpy.QtWidgets import QTreeView, QWidget, QLabel, QPushButton, QVBoxLayout

from .. import utils
from ..game import GameManager

debug = utils.Logger.debug()


class ProcessSelectModel(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.source_model = QStandardItemModel(parent)
        self.source_model.setColumnCount(3)

        self.source_model.setHeaderData(0, Qt.Horizontal, self.tr("Directory"), Qt.DisplayRole)
        self.source_model.setHeaderData(1, Qt.Horizontal, self.tr("Name"), Qt.DisplayRole)
        self.source_model.setHeaderData(2, Qt.Horizontal, self.tr("Location"), Qt.DisplayRole)


class ProcessSelectView(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tree_view = QTreeView(parent)
        self.tree_view.setAlternatingRowColors(True)


class ProcessSelectController(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ProcessSelectModel(parent).source_model
        self._view = ProcessSelectView(parent).tree_view
        self._view.setModel(self._model)

    @Slot()
    def update(self):
        # self._model.clear()
        self._model.setRowCount(0)
        for process in utils.windows_iter():
            self._model.insertRow(0)
            self._model.setData(self._model.index(0, 0), process.dir,  Qt.DisplayRole)
            self._model.setData(self._model.index(0, 1), process.name, Qt.DisplayRole)
            self._model.setData(self._model.index(0, 1), process.icon, Qt.DecorationRole)
            self._model.setData(self._model.index(0, 1), process.pid,  Qt.ToolTipRole)
            self._model.setData(self._model.index(0, 2), process.path, Qt.DisplayRole)

    def view(self):
        return self._view

    @Slot()
    def send_path(self):
        index = self._view.currentIndex()
        path = self._model.item(index.row(), 2).text()

        debug(f'send {path} to GameManager')
        GameManager.instance(path)


class ProcessSelectPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent

        self.control = ProcessSelectController(self)
        self.control.update()

        self._init_ui()
        self._connect()

    def _init_ui(self):
        self._parent.setWindowTitle("Select game process")

        intro_label = QLabel("Please select game process")
        intro_label.setWordWrap(True)

        self.refresh_button = QPushButton("Refresh")
        self.next_button = QPushButton(self.tr("Next"))

        layout = QVBoxLayout()
        layout.addWidget(intro_label)
        layout.addWidget(self.control.view())
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def _connect(self):
        self.refresh_button.clicked.connect(self.control.update)
        self.next_button.clicked.connect(self.control.send_path)
        self.next_button.clicked.connect(self._parent.hide)
        self.next_button.clicked.connect(self._parent.open_filter)
