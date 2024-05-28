import sys
import os
from PySide6.QtCore import QProcess, QObject, QUrl, QCoreApplication
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtGui import QGuiApplication, Qt
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
import FluentUI


from common import SettingsHelper, AppInfo, TranslateHelper
import common.Log as Log

import example_rc as rc

qApp: QGuiApplication


def main():
    SettingsHelper().app_path = sys.path[0]

    os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=2'
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"

    QGuiApplication.setOrganizationName("ZhuZiChu")
    QGuiApplication.setOrganizationDomain("https://zhuzichu520.github.io")
    QGuiApplication.setApplicationName("FluentUI")
    QGuiApplication.setApplicationDisplayName("FluentUI Example")
    QGuiApplication.setApplicationVersion(AppInfo().applicationversion)
    QGuiApplication.setQuitOnLastWindowClosed(False)


    Log.setup(sys.argv, AppInfo().appname)
    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)

    """print(SettingsHelper().getUseSystemAppBar())
    print(SettingsHelper().getLanguage())
    print(SettingsHelper().getDarkMode())
    SettingsHelper().saveUseSystemAppBar(True)
    print(SettingsHelper().getUseSystemAppBar())
    print(TranslateHelper().current)"""

    app = QGuiApplication(sys.argv)
    #qmlRegisterType(OpenGLItem,'example',1,0,'OpenGLItem')

    print('111')
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("AppInfo", AppInfo())
    engine.rootContext().setContextProperty("SettingsHelper",SettingsHelper())
    engine.rootContext().setContextProperty("TranslateHelper",TranslateHelper())
    engine.rootContext().setContextProperty("FluTools", FluentUI.FluTools())
    engine.rootContext().setContextProperty("FluColors", FluentUI.FluColors())
    engine.rootContext().setContextProperty("FluApp", FluentUI.FluApp())
    engine.rootContext().setContextProperty("FluTextStyle", FluentUI.FluTextStyle())
    engine.rootContext().setContextProperty("FluTheme", FluentUI.FluTheme())
    print('222')

    TranslateHelper().engine = engine
    print(engine.importPathList())
    qml_file = "qrc:/ui/App.qml"
    url = QUrl(qml_file)

    def handle_object_created(obj, obj_url):
        if obj is None and url == obj_url:
            qApp.exit(-1)

    engine.objectCreated.connect(handle_object_created, Qt.ConnectionType.QueuedConnection)
    engine.load(url)
    """if not engine.rootObjects():
        qApp.exit(-1)"""

    exec_ = qApp.exec()
    match exec_:
        case 931:
            # QGuiApplication.applicationFilePath()需要打包成exe后才能正确的路径重启，不然这个函数获取的路径是python的路径
            QProcess.startDetached(qApp.applicationFilePath(), qApp.arguments()[1:])
        case _:
            sys.exit(exec_)


if __name__ == '__main__':
    main()
