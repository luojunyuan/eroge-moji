from PySide.QtDeclarative import qmlRegisterType

from .text import TextManagerQMLPlugin


def register_qml_type():
    qmlRegisterType(TextManagerQMLPlugin, 'eroge.moji', 1, 0, 'ReciveText')
