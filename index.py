import sys
import UiToPy
from PyQt5 import QtWidgets


if __name__ == "__main__":
    UiToPy.convert_ui_to_py()
    from application import Main

    qt = QtWidgets.QApplication(sys.argv)
    app = Main()
    app.show()
    qt.exec_()
