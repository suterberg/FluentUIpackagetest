import os

from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQml import QQmlApplicationEngine, QmlNamedElement, QmlSingleton

from FluentUI import singleton




APPLICATION_FULL_VERSION = '1.0.0'
VERSION_COUNTER = 1
COMMIT_HASH = '1.0.0'
APPLICATION_VERSION = '1.0.0'


def readVersion():
    path2 = os.path.dirname(os.path.dirname(__file__))
    #print(path2)
    files = os.path.join(path2, 'Version.h')
    #print(files)
    with open(files, 'r') as f:
        while code := f.readline():
            if code.startswith("#define"):
                mm = code.strip('\n').split(" ")
                if len(mm) > 2:
                    pp = f'{mm[1]} = {mm[2]}'
                    globals()[mm[1]] = mm[2]


@singleton
class AppInfo(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        readVersion()
        self._version = APPLICATION_VERSION
        self.versionCounter = VERSION_COUNTER
        self.applicationversion = APPLICATION_VERSION
        self.applicationfullversion = APPLICATION_FULL_VERSION
        self.commit_hash = COMMIT_HASH
        self.appname = "example"

    versionChanged = Signal(str)

    @Property(str, notify=versionChanged)
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        self._version = value
        self.versionChanged.emit(value)

    @Slot()
    def testCrash(self):
        raise ValueError


if __name__ == '__main__':
    cc = AppInfo()
