import sys
from application import Main
from UiToPy import convert
from PyQt5 import QtWidgets



if __name__ == "__main__":
    convert()
    qt = QtWidgets.QApplication(sys.argv)
    app = Main()
    app.show()
    qt.exec_()