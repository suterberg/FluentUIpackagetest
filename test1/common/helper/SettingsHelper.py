# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject, Slot, QStandardPaths, QSettings, QFileInfo
from PySide6.QtQml import QmlNamedElement, QmlSingleton

from FluentUI import singleton



@singleton
class SettingsHelper(QObject):
    def __init__(self, par=None,args=None):
        super().__init__(parent=par)
        self._settings = QSettings()
    @property
    def app_path(self):
        return

    @app_path.setter
    def app_path(self, value):
        applicationPath = value
        fileInfo = QFileInfo(applicationPath)
        iniFileName = fileInfo.completeBaseName() + '.ini'
        iniFilePath = QStandardPaths.writableLocation(
            QStandardPaths.AppLocalDataLocation) + "/" + iniFileName
        print(f'ini Path\t\t{iniFilePath}')
        self._settings = QSettings(iniFilePath, QSettings.IniFormat)
        print(self._settings)
        self.save('darkMode', self.getDarkMode())
        self.save('useSystemAppBar', self.getUseSystemAppBar())
        self.save('language', self.getLanguage())


    def save(self, key: str, val):
        self._settings.setValue(key, val)

    def get(self, key: str, default):
        data = self._settings.value(key)
        if data:
            return data
        else:
            return default

    @Slot(result=int)
    def getDarkMode(self):
        return int(self.get("darkMode", 0))

    @Slot(int)
    def saveDarkMode(self, darkMode: int):
        self.save("darkMode", darkMode)

    @Slot(result=bool)
    def getUseSystemAppBar(self):
        return bool(self.get('useSystemAppBar', 'false')=='true')

    @Slot(bool)
    def saveUseSystemAppBar(self, useSystemAppBar: bool):
        self.save("useSystemAppBar", useSystemAppBar)

    @Slot(result=str)
    def getLanguage(self):
        return str(self.get('language', "en_US"))

    @Slot(str)
    def saveLanguage(self, language: str):
        self.save("language", language)
