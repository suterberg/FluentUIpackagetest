from PySide6.QtCore import QObject, Slot, QStandardPaths, QSettings, Signal, Property, QTranslator
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlNamedElement, QmlSingleton, QQmlEngine

from FluentUI import singleton
from .SettingsHelper import SettingsHelper
import os



qApp: QGuiApplication


@ singleton
class TranslateHelper(QObject):
    currentChanged = Signal()
    languagesChanged = Signal()

    def __init__(self, par=None):
        super().__init__(parent=par)
        self._current = SettingsHelper().getLanguage()
        self._languages = ["en_US", "zh_CN"]
        self._engine = None
        self._translator = None

    @property
    def engine(self):
        return None

    @engine.setter
    def engine(self, value: QQmlEngine):
        self._engine = value
        self._translator = QTranslator(self)
        QGuiApplication.installTranslator(self._translator)
        paths1 = os.getcwd() + "\\i18n"
        translatorPath = QGuiApplication.applicationDirPath() + "/i18n"
        print(paths1)
        if self._translator.load(f'{paths1}\\example_{self._current}.qm'):
            self._engine.retranslate()
        else:
            print(self._current)

    @Property(str, notify=currentChanged)
    def current(self) -> str:
        return self._current

    @current.setter
    def current(self, value: str):
        self._current = value
        self.currentChanged.emit()

    @Property(list, notify=languagesChanged)
    def languages(self) -> list:
        return self._languages

    @languages.setter
    def languages(self, value: list):
        self._languages = value
        self.languagesChanged.emit()

    def init(self):
        iniFileName = "example.ini"
        iniFilePath = QStandardPaths.writableLocation(
            QStandardPaths.AppLocalDataLocation) + "/" + iniFileName
        self._settings = QSettings(iniFilePath, QSettings.IniFormat)

    def _save(self, key, val):
        self._settings.setValue(key, val)

    def _get(self, key, default):
        data = self._settings.value(key)
        if data is None:
            return default
        return data

    @Slot(result=int)
    def getDarkMode(self):
        return int(self._get("darkMode", 0))

    @Slot(int)
    def saveDarkMode(self, darkMode: int):
        self._save("darkMode", darkMode)

    @Slot(result=bool)
    def getUseSystemAppBar(self):
        return bool(self._get('useSystemAppBar', "false") == "true")

    @Slot(bool)
    def saveUseSystemAppBar(self, useSystemAppBar: bool):
        self._save("useSystemAppBar", useSystemAppBar)
