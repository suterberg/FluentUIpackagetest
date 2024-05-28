import enum
import os

from PySide6 import QtQml
from PySide6.QtCore import QObject, Property, Signal, Slot, QEnum
from PySide6.QtQml import QQmlApplicationEngine, QmlNamedElement, QmlSingleton, QJSValue

from FluentUI import singleton


@QtQml.QmlNamedElement("NetworkType")
@QtQml.QmlUncreatable("Enum is not a type")
class NetworkType(QObject):
    class CacheMode(enum.Enum):
        NoCache = 0x0000
        RequestFailedReadCache = 0x0001
        IfNoneCacheRequest = 0x0002
        FirstCacheThenRequest = 0x0004

    QEnum(CacheMode)


@QtQml.QmlNamedElement("NetworkCallable")
class NetworkCallable(QObject):
    start = Signal()
    finish = Signal()
    error = Signal(int, str, str)
    success = Signal(str)
    cached = Signal(str)
    uploadProgress = Signal(int, int)
    downloadProgress = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)


class FluDownloadParam(QObject):
    def __init__(self, destPath: str, append: bool, parent=None):
        super().__init__(parent)
        self._destPath = destPath
        self._append = append


class NetworkParam(QObject):
    class Method(enum.Enum):
        METHOD_GET = 0
        METHOD_HEAD = 1
        METHOD_POST = 2
        METHOD_PUT = 3
        METHOD_PATCH = 4
        METHOD_DELETE = 5

    class Type(enum.Enum):
        TYPE_NONE = 0
        TYPE_FORM = 1
        TYPE_JSON = 2
        TYPE_JSONARRAY = 3
        TYPE_BODY = 4

    def __init__(self, url: str = '', type_: Type = 4, method: Method = 0, parent=None):
        super().__init__(parent)
        self._downloadParam: FluDownloadParam = None
        self._target: QObject = None
        self._type: NetworkParam.Type = type_
        self._method: NetworkParam.Method = method
        self._url: str = url
        self._body: str = ''
        self._queryMap = {}
        self._headerMap = {}
        self._paramMap = {}
        self._fileMap = {}
        self._timeout = -1
        self._retry = -1
        self._openLog = None
        self._cacheMode = NetworkType.CacheMode.NoCache.value

    @Slot(str, 'QVariant')
    def addQuery(self, key, value):
        pass

    @Slot(str, 'QVariant')
    def addHeader(self, key, value):
        pass

    @Slot(str, 'QVariant')
    def add(self):
        pass

    @Slot(str, 'QVariant')
    def addFile(self, key, value):
        pass

    @Slot(str)
    def setBody(self, val):
        pass

    @Slot(int)
    def setTimeout(self, timeout):
        pass

    @Slot(int)
    def setRetry(self, retry):
        pass

    @Slot(int)
    def setCacheMode(self, mode):
        pass

    @Slot(str)
    @Slot(str, bool)
    def toDownload(self, destPath, append=False):
        pass

    @Slot(QObject)
    def bind(self, target):
        pass

    @Slot('QVariant')
    def openLog(self, val):
        pass

    @Slot(NetworkCallable)
    def go(self, result):
        pass

    def buildCacheKey(self):
        pass

    def method2String(self):
        pass

    def getTimeout(self):
        pass

    def getRetry(self):
        pass

    def getOpenLog(self):
        pass


@singleton
@QtQml.QmlNamedElement("NetworkCallable")
@QtQml.QmlSingleton
class NetWork(QObject):
    timeoutChanged = Signal()
    retryChanged = Signal()
    cacheDirChanged = Signal()
    openLogChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timeout = int()
        self._retry = int()
        self._cacheDir = str()
        self._openLog = bool()

    @Property(bool, notify=openLogChanged)
    def openLog(self) -> bool:
        return self._openLog

    @openLog.setter
    def openLog(self, value: bool):
        self._openLog = value
        self.openLogChanged.emit()

    @Property(str, notify=cacheDirChanged)
    def cacheDir(self) -> str:
        return self._cacheDir

    @cacheDir.setter
    def cacheDir(self, value: str):
        self._cacheDir = value
        self.cacheDirChanged.emit()

    @Property(int, notify=retryChanged)
    def retry(self) -> int:
        return self._retry

    @retry.setter
    def retry(self, value: int):
        self._retry = value
        self.retryChanged.emit()

    @Property(int, notify=timeoutChanged)
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value
        self.timeoutChanged.emit()

    @Slot(str)
    def get(self, url):
        pass

    @Slot(str)
    def head(self, url):
        pass

    @Slot(str)
    def postBody(self, url):
        pass

    @Slot(str)
    def putBody(self, url):
        pass

    @Slot(str)
    def patchBody(self, url):
        pass

    @Slot(str)
    def deleteBody(self, url):
        pass

    @Slot(str)
    def postForm(self, url):
        pass

    @Slot(str)
    def putForm(self, url):
        pass

    @Slot(str)
    def patchForm(self, url):
        pass

    @Slot(str)
    def deleteForm(self, url):
        pass

    @Slot(str)
    def postJson(self, url):
        pass

    @Slot(str)
    def putJson(self, url):
        pass

    @Slot(str)
    def patchJson(self, url):
        pass

    @Slot(str)
    def deleteJson(self, url):
        pass

    @Slot(str)
    def postJsonArray(self, url):
        pass

    @Slot(str)
    def putJsonArray(self, url):
        pass

    @Slot(str)
    def patchJsonArray(self, url):
        pass

    @Slot(str)
    def deleteJsonArray(self, url):
        pass

    @Slot(QJSValue)
    def setInterceptor(self, interceptor):
        pass

    def handle(self, params: NetworkParam, result: NetworkCallable):
        pass

    def handleDownload(self, params: NetworkParam, result: NetworkCallable):
        pass
