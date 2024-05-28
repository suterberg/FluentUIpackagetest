from FluentUI.common import *
import FluentUI.fluentui_rc as rc
from FluentUI.ui import *
from FluentUI.item import *
from FluentUI.model import *

if __name__ == '__main__':
    from FluentUI.script_make_rcc import run as make_rcc
    from FluentUI.script_make_qml import run as make_qmldir
    from FluentUI.script_make_ts import run as make_ts

    make_qmldir()
    make_ts()
    make_rcc()
