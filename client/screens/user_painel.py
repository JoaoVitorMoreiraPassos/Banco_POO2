# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/3_user_painel.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1373, 768)
                font = QtGui.QFont()
                font.setFamily("Tlwg Mono")
                MainWindow.setFont(font)
                MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
                MainWindow.setStyleSheet("background-color: #498f97")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout.setObjectName("gridLayout")
                self.frame = QtWidgets.QFrame(self.centralwidget)
                self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
                self.frame.setStyleSheet("border: 0px")
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setLineWidth(0)
                self.frame.setObjectName("frame")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.label_2 = QtWidgets.QLabel(self.frame)
                self.label_2.setMaximumSize(QtCore.QSize(16777215, 55))
                font = QtGui.QFont()
                font.setFamily("Suruma")
                font.setPointSize(41)
                self.label_2.setFont(font)
                self.label_2.setStyleSheet("")
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
                self.label = QtWidgets.QLabel(self.frame)
                self.label.setMaximumSize(QtCore.QSize(16777215, 71))
                font = QtGui.QFont()
                font.setFamily("DejaVu Serif")
                font.setPointSize(25)
                self.label.setFont(font)
                self.label.setStyleSheet("color: #fff;\n"
        "")
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
                self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
                self.frame_2 = QtWidgets.QFrame(self.centralwidget)
                self.frame_2.setMaximumSize(QtCore.QSize(16777215, 400))
                self.frame_2.setStyleSheet("border: 0px")
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.widget_2 = QtWidgets.QWidget(self.frame_2)
                self.widget_2.setMaximumSize(QtCore.QSize(16777215, 150))
                self.widget_2.setObjectName("widget_2")
                self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_2)
                self.gridLayout_5.setObjectName("gridLayout_5")
                self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
                self.pushButton_5.setMaximumSize(QtCore.QSize(301, 110))
                font = QtGui.QFont()
                font.setFamily("Sans Serif")
                font.setPointSize(17)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                font.setStrikeOut(False)
                self.pushButton_5.setFont(font)
                self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.pushButton_5.setStyleSheet("\n"
        "QPushButton {\n"
        "\n"
        "    color: #fff;\n"
        "    border-radius: 10px;\n"
        "    background-color: #7cbec6\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(140, 214, 223);\n"
        "    border: 1px groove rgb(140, 214, 223);\n"
        "}")
                self.pushButton_5.setObjectName("pushButton_5")
                self.gridLayout_5.addWidget(self.pushButton_5, 0, 0, 1, 1)
                self.gridLayout_3.addWidget(self.widget_2, 1, 0, 1, 1)
                self.widget = QtWidgets.QWidget(self.frame_2)
                self.widget.setMaximumSize(QtCore.QSize(16777215, 150))
                self.widget.setStyleSheet("border: 0px")
                self.widget.setObjectName("widget")
                self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
                self.gridLayout_4.setObjectName("gridLayout_4")
                self.pushButton_2 = QtWidgets.QPushButton(self.widget)
                self.pushButton_2.setMaximumSize(QtCore.QSize(299, 110))
                font = QtGui.QFont()
                font.setFamily("Sans Serif")
                font.setPointSize(17)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                font.setStrikeOut(False)
                self.pushButton_2.setFont(font)
                self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.pushButton_2.setStyleSheet("\n"
        "QPushButton {\n"
        "\n"
        "    color: #fff;\n"
        "    border-radius: 10px;\n"
        "    background-color: #7cbec6\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(140, 214, 223);\n"
        "    border: 1px groove rgb(140, 214, 223);\n"
        "}")
                self.pushButton_2.setObjectName("pushButton_2")
                self.gridLayout_4.addWidget(self.pushButton_2, 0, 0, 1, 1)
                self.pushButton_3 = QtWidgets.QPushButton(self.widget)
                self.pushButton_3.setMaximumSize(QtCore.QSize(299, 110))
                font = QtGui.QFont()
                font.setFamily("Sans Serif")
                font.setPointSize(17)
                font.setBold(False)
                font.setItalic(False)
                font.setWeight(50)
                font.setStrikeOut(False)
                self.pushButton_3.setFont(font)
                self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.pushButton_3.setStyleSheet("\n"
        "QPushButton {\n"
        "\n"
        "    color: #fff;\n"
        "    border-radius: 10px;\n"
        "    background-color: #7cbec6\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(140, 214, 223);\n"
        "    border: 1px groove rgb(140, 214, 223);\n"
        "}")
                self.pushButton_3.setObjectName("pushButton_3")
                self.gridLayout_4.addWidget(self.pushButton_3, 0, 1, 1, 1)
                self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)
                self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
                MainWindow.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Dashboard"))
                self.label_2.setText(_translate("MainWindow", "Beast Bank"))
                self.label.setText(_translate("MainWindow", "Olá, Cliente"))
                self.pushButton_5.setText(_translate("MainWindow", "LogOut"))
                self.pushButton_2.setText(_translate("MainWindow", "Criar conta corrente"))
                self.pushButton_3.setText(_translate("MainWindow", "Criar conta poupança"))
