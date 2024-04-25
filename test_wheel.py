# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

'''Test cases for connecting signals between threads'''

import PySide6
from PySide6.QtCore import QThread, QTimer, QObject, Signal, Slot, QCoreApplication, __version__

print(PySide6.__version__)
print(PySide6.QtCore.__version__)


class Source(QObject):
    source = Signal()

    def __init__(self, *args):
        super().__init__(*args)

    @Slot()
    def emit_sig(self):
        self.source.emit()


class Target(QObject):
    def __init__(self, *args):
        super().__init__(*args)
        self.called = False

    @Slot()
    def myslot(self):
        self.called = True


class ThreadJustConnects(QThread):
    def __init__(self, source, *args):
        super().__init__(*args)
        self.source = source
        self.target = Target()

    def run(self):
        self.source.source.connect(self.target.myslot)
        self.source.source.connect(self.quit)
        self.exec()


def test_signal():
    app = QCoreApplication([])
    source = Source()
    thread = ThreadJustConnects(source)

    thread.finished.connect(QCoreApplication.quit)
    thread.start()

    QTimer.singleShot(50, source.emit_sig)
    app.exec()
    thread.wait()

    assert thread.target.called
