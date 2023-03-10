from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """
        Este é o painel de conta do usuário, onde ele pode ver o saldo, o número da conta e o tipo da conta.

        ...

        Attributes
        ----------
        MainWindow : QMainWindow
                A tela principal do programa.

        Methods
        -------
        setupUi(MainWindow)
            Este método configura a tela de acordo com o arquivo .ui.
        retranslateUi(MainWindow)
            Este método configura o texto de acordo com o arquivo .ui.   
    """    
    def setupUi(self, MainWindow):
        """
        Esse método configura a tela de acordo com o arquivo .ui.

        Parameters
        ----------
        MainWindow : QMainWindow
                A tela principal do programa.
        
        Returns
        -------
        None
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setStyleSheet("background-color: #498f97;\n"
"\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 131))
        self.frame.setStyleSheet("border-bottom: 1px;\n"
"border-top: 0px;\n"
"border-left: 0px;\n"
"border-right: 0px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setMinimumSize(QtCore.QSize(300, 111))
        self.widget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tipo = QtWidgets.QLabel(self.widget)
        self.tipo.setMinimumSize(QtCore.QSize(181, 31))
        self.tipo.setMaximumSize(QtCore.QSize(181, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tipo.setFont(font)
        self.tipo.setStyleSheet("color: #fff;")
        self.tipo.setText("")
        self.tipo.setAlignment(QtCore.Qt.AlignCenter)
        self.tipo.setObjectName("tipo")
        self.gridLayout_3.addWidget(self.tipo, 0, 0, 1, 1)
        self.numero = QtWidgets.QLabel(self.widget)
        self.numero.setMinimumSize(QtCore.QSize(181, 31))
        self.numero.setMaximumSize(QtCore.QSize(181, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.numero.setFont(font)
        self.numero.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.numero.setStyleSheet("color: #fff;")
        self.numero.setText("")
        self.numero.setAlignment(QtCore.Qt.AlignCenter)
        self.numero.setObjectName("numero")
        self.gridLayout_3.addWidget(self.numero, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setMinimumSize(QtCore.QSize(356, 111))
        self.widget_2.setMaximumSize(QtCore.QSize(356, 111))
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.saldo = QtWidgets.QLineEdit(self.widget_2)
        self.saldo.setMinimumSize(QtCore.QSize(291, 61))
        self.saldo.setMaximumSize(QtCore.QSize(291, 61))
        self.saldo.setStyleSheet("background-color: #fff;\n"
"border-radius: 5px;\n"
"padding-left: 10px;\n"
"padding-right: 10px;")
        self.saldo.setText("")
        self.saldo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.saldo.setDragEnabled(False)
        self.saldo.setReadOnly(True)
        self.saldo.setObjectName("saldo")
        self.gridLayout_4.addWidget(self.saldo, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox.setMinimumSize(QtCore.QSize(121, 20))
        self.checkBox.setMaximumSize(QtCore.QSize(121, 20))
        self.checkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBox.setStyleSheet("background-color: #498f97;\n"
"color: white;")
        self.checkBox.setChecked(True)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_4.addWidget(self.checkBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 2, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setStyleSheet("border: 0px\n"
"")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout.addWidget(self.frame_4, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("border: 0px")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.btn_sair = QtWidgets.QPushButton(self.frame_2)
        self.btn_sair.setMinimumSize(QtCore.QSize(171, 0))
        self.btn_sair.setMaximumSize(QtCore.QSize(300, 90))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_sair.setFont(font)
        self.btn_sair.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sair.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"    color: #fff;\n"
"    border-radius: 10px;\n"
"    background-color: #13747d;\n"
"    \n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(86, 132, 137);\n"
"    border: 1px solid #7cbec6 ;\n"
"}")
        self.btn_sair.setObjectName("btn_sair")
        self.gridLayout_6.addWidget(self.btn_sair, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 4, 0, 1, 1)
        self.frame_option = QtWidgets.QFrame(self.centralwidget)
        self.frame_option.setStyleSheet("border: 0px")
        self.frame_option.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_option.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_option.setObjectName("frame_option")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_option)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget_transf = QtWidgets.QWidget(self.frame_option)
        self.widget_transf.setMinimumSize(QtCore.QSize(171, 171))
        self.widget_transf.setMaximumSize(QtCore.QSize(171, 171))
        self.widget_transf.setObjectName("widget_transf")
        self.img_transf = QtWidgets.QLabel(self.widget_transf)
        self.img_transf.setGeometry(QtCore.QRect(60, 100, 50, 50))
        self.img_transf.setStyleSheet("border-radius:20px;\n"
"background-color: rgba(191, 64, 64, 0)")
        self.img_transf.setText("")
        self.img_transf.setObjectName("img_transf")
        self.transferencia = QtWidgets.QPushButton(self.widget_transf)
        self.transferencia.setGeometry(QtCore.QRect(10, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.transferencia.setFont(font)
        self.transferencia.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.transferencia.setStyleSheet("QPushButton {\n"
"    color: #fff;\n"
"    background-color: rgba(200, 200, 200, 0);\n"
"\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.transferencia.setObjectName("transferencia")
        self.transferencia_back = QtWidgets.QPushButton(self.widget_transf)
        self.transferencia_back.setGeometry(QtCore.QRect(10, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.transferencia_back.setFont(font)
        self.transferencia_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.transferencia_back.setStyleSheet("QPushButton {\n"
"\n"
"    background-color: #7cbec6;\n"
"    color: #fff;\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(140, 214, 223);\n"
"    border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.transferencia_back.setText("")
        self.transferencia_back.setObjectName("transferencia_back")
        self.transferencia_back.raise_()
        self.img_transf.raise_()
        self.transferencia.raise_()
        self.gridLayout_5.addWidget(self.widget_transf, 0, 2, 1, 1)
        self.widget_dep = QtWidgets.QWidget(self.frame_option)
        self.widget_dep.setMinimumSize(QtCore.QSize(171, 171))
        self.widget_dep.setMaximumSize(QtCore.QSize(171, 171))
        self.widget_dep.setObjectName("widget_dep")
        self.img_dep = QtWidgets.QLabel(self.widget_dep)
        self.img_dep.setGeometry(QtCore.QRect(60, 100, 50, 50))
        self.img_dep.setStyleSheet("border-radius:20px;\n"
"background-color: rgba(191, 64, 64, 0)")
        self.img_dep.setText("")
        self.img_dep.setObjectName("img_dep")
        self.deposito_back = QtWidgets.QPushButton(self.widget_dep)
        self.deposito_back.setGeometry(QtCore.QRect(10, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.deposito_back.setFont(font)
        self.deposito_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deposito_back.setStyleSheet("QPushButton {\n"
"\n"
"    background-color: #7cbec6;\n"
"    color: #fff;\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(140, 214, 223);\n"
"    border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.deposito_back.setText("")
        icon = QtGui.QIcon.fromTheme("icones/to_left.png")
        self.deposito_back.setIcon(icon)
        self.deposito_back.setObjectName("deposito_back")
        self.deposito = QtWidgets.QPushButton(self.widget_dep)
        self.deposito.setGeometry(QtCore.QRect(10, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.deposito.setFont(font)
        self.deposito.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deposito.setStyleSheet("QPushButton {\n"
"    color: #fff;\n"
"    background-color: rgba(200, 200, 200, 0);\n"
"\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.deposito.setObjectName("deposito")
        self.deposito_back.raise_()
        self.img_dep.raise_()
        self.deposito.raise_()
        self.gridLayout_5.addWidget(self.widget_dep, 0, 0, 1, 1)
        self.widget_saque = QtWidgets.QWidget(self.frame_option)
        self.widget_saque.setMinimumSize(QtCore.QSize(171, 171))
        self.widget_saque.setMaximumSize(QtCore.QSize(171, 171))
        self.widget_saque.setObjectName("widget_saque")
        self.img_saque = QtWidgets.QLabel(self.widget_saque)
        self.img_saque.setGeometry(QtCore.QRect(60, 100, 50, 50))
        self.img_saque.setMinimumSize(QtCore.QSize(50, 50))
        self.img_saque.setMaximumSize(QtCore.QSize(50, 50))
        self.img_saque.setStyleSheet("border-radius:20px;\n"
"background-color: rgba(191, 64, 64, 0)")
        self.img_saque.setText("")
        self.img_saque.setObjectName("img_saque")
        self.saque_back = QtWidgets.QPushButton(self.widget_saque)
        self.saque_back.setGeometry(QtCore.QRect(10, 10, 150, 150))
        self.saque_back.setMinimumSize(QtCore.QSize(150, 150))
        self.saque_back.setMaximumSize(QtCore.QSize(150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.saque_back.setFont(font)
        self.saque_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saque_back.setStyleSheet("QPushButton {\n"
"\n"
"    background-color: #7cbec6;\n"
"    color: #fff;\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(140, 214, 223);\n"
"    border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.saque_back.setText("")
        self.saque_back.setObjectName("saque_back")
        self.saque = QtWidgets.QPushButton(self.widget_saque)
        self.saque.setGeometry(QtCore.QRect(10, 10, 150, 150))
        self.saque.setMinimumSize(QtCore.QSize(150, 150))
        self.saque.setMaximumSize(QtCore.QSize(150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.saque.setFont(font)
        self.saque.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saque.setStyleSheet("QPushButton {\n"
"    color: #fff;\n"
"    background-color: rgba(200, 200, 200, 0);\n"
"\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.saque.setObjectName("saque")
        self.saque_back.raise_()
        self.img_saque.raise_()
        self.saque.raise_()
        self.gridLayout_5.addWidget(self.widget_saque, 0, 1, 1, 1)
        self.widget_extrato = QtWidgets.QWidget(self.frame_option)
        self.widget_extrato.setMinimumSize(QtCore.QSize(181, 171))
        self.widget_extrato.setMaximumSize(QtCore.QSize(181, 171))
        self.widget_extrato.setObjectName("widget_extrato")
        self.img_extrato = QtWidgets.QLabel(self.widget_extrato)
        self.img_extrato.setGeometry(QtCore.QRect(70, 100, 50, 50))
        self.img_extrato.setStyleSheet("background-color: rgba(191, 64, 64, 0);\n"
"border-radius:20px")
        self.img_extrato.setText("")
        self.img_extrato.setObjectName("img_extrato")
        self.extrato_back = QtWidgets.QPushButton(self.widget_extrato)
        self.extrato_back.setGeometry(QtCore.QRect(20, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.extrato_back.setFont(font)
        self.extrato_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.extrato_back.setStyleSheet("QPushButton {\n"
"\n"
"    background-color: #7cbec6;\n"
"    color: #fff;\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(140, 214, 223);\n"
"    border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.extrato_back.setText("")
        self.extrato_back.setObjectName("extrato_back")
        self.extrato = QtWidgets.QPushButton(self.widget_extrato)
        self.extrato.setGeometry(QtCore.QRect(20, 10, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.extrato.setFont(font)
        self.extrato.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.extrato.setStyleSheet("QPushButton {\n"
"    color: #fff;\n"
"    background-color: rgba(200, 200, 200, 0);\n"
"\n"
"    border-radius: 75px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border: 10px groove rgb(140, 214, 223);\n"
"}")
        self.extrato.setObjectName("extrato")
        self.extrato_back.raise_()
        self.img_extrato.raise_()
        self.extrato.raise_()
        self.gridLayout_5.addWidget(self.widget_extrato, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.frame_option, 3, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_3.setStyleSheet("border: 0px\n"
"")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setFamily("Suruma")
        font.setPointSize(41)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Método para traduzir os textos da interface

        Parameters
        ----------
        MainWindow : QMainWindow
                Janela principal da interface.
        
        Returns
        -------
        None
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Contas"))
        self.checkBox.setText(_translate("MainWindow", "mostrar saldo"))
        self.btn_sair.setText(_translate("MainWindow", "Sair"))
        self.transferencia.setText(_translate("MainWindow", "Transferência"))
        self.deposito.setText(_translate("MainWindow", "Depósito"))
        self.saque.setText(_translate("MainWindow", "Saque"))
        self.extrato.setText(_translate("MainWindow", "Extrato"))
        self.label_2.setText(_translate("MainWindow", "Beast Bank"))
