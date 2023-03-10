from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
        """
        Este é o código gerado pelo Qt Designer, para a tela de criar conta do usuário no banco.

        ...

        Attributes
        ----------
        MainWindow : QMainWindow
                Janela principal da tela de criar conta do usuário no banco.
        
        Methods
        -------
        setupUi(MainWindow)
                Configura a tela de criar conta do usuário no banco.
        retranslateUi(MainWindow)
                Traduz a tela de criar conta do usuário no banco.
        """
        def setupUi(self, MainWindow):
                """
                Configura a tela de criar conta do usuário no banco.

                Parameters
                ----------
                MainWindow : QMainWindow
                        Janela principal da tela de criar conta do usuário no banco.
                
                Returns
                -------
                None
                """
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1366, 768)
                MainWindow.setStyleSheet("background-color: #498f97;\n"
        "\n"
        "")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout.setObjectName("gridLayout")
                self.frame_2 = QtWidgets.QFrame(self.centralwidget)
                self.frame_2.setMaximumSize(QtCore.QSize(16777215, 40))
                self.frame_2.setStyleSheet("border: 0px")
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.voltar = QtWidgets.QPushButton(self.frame_2)
                self.voltar.setGeometry(QtCore.QRect(40, 0, 40, 40))
                self.voltar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.voltar.setStyleSheet("background-color: rgba(200, 200, 200, 51);\n"
        "border-radius: 20px;\n"
        "")
                self.voltar.setText("")
                self.voltar.setObjectName("voltar")
                self.img = QtWidgets.QLabel(self.frame_2)
                self.img.setGeometry(QtCore.QRect(40, 0, 40, 40))
                self.img.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.img.setStyleSheet("background-color: rgb(243, 243, 243);\n"
        "border-radius: 20px;")
                self.img.setText("")
                self.img.setAlignment(QtCore.Qt.AlignCenter)
                self.img.setObjectName("img")
                self.img.raise_()
                self.voltar.raise_()
                self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
                self.frame_3 = QtWidgets.QFrame(self.centralwidget)
                self.frame_3.setStyleSheet("border: 0px")
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.frame = QtWidgets.QFrame(self.frame_3)
                self.frame.setMinimumSize(QtCore.QSize(361, 411))
                self.frame.setMaximumSize(QtCore.QSize(361, 411))
                self.frame.setStyleSheet("background-color: #156068;\n"
        "border-radius: 10px\n"
        "\n"
        "")
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame")
                self.Titulo = QtWidgets.QLabel(self.frame)
                self.Titulo.setGeometry(QtCore.QRect(50, 60, 261, 81))
                font = QtGui.QFont()
                font.setPointSize(29)
                font.setBold(False)
                font.setWeight(50)
                self.Titulo.setFont(font)
                self.Titulo.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.Titulo.setStyleSheet("color: #fff;\n"
        "font-size: 26;")
                self.Titulo.setAlignment(QtCore.Qt.AlignCenter)
                self.Titulo.setWordWrap(True)
                self.Titulo.setObjectName("Titulo")
                self.btn_criar = QtWidgets.QPushButton(self.frame)
                self.btn_criar.setGeometry(QtCore.QRect(50, 295, 261, 35))
                self.btn_criar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_criar.setStyleSheet("QPushButton {\n"
        "\n"
        "    background-color: #498f97;\n"
        "    border-radius: 17px;\n"
        "    color: #fff\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(86, 159, 168);\n"
        "\n"
        "}")
                self.btn_criar.setObjectName("btn_criar")
                self.label_2 = QtWidgets.QLabel(self.frame)
                self.label_2.setGeometry(QtCore.QRect(110, 20, 141, 31))
                font = QtGui.QFont()
                font.setFamily("Sawasdee")
                font.setPointSize(20)
                self.label_2.setFont(font)
                self.label_2.setStyleSheet("color: #7cbec6;")
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.senha = QtWidgets.QLineEdit(self.frame)
                self.senha.setGeometry(QtCore.QRect(50, 220, 261, 35))
                self.senha.setStyleSheet("QLineEdit{\n"
        "    background-color: #fff;\n"
        "    color: #111;\n"
        "    padding-left: 5px;\n"
        "    border-radius: 17px;\n"
        "    border: 2px solid #498f97;\n"
        "}\n"
        "\n"
        "QLineEdit:focus{\n"
        "    border: 2px ridge rgb(3, 151, 136)\n"
        "}")
                self.senha.setEchoMode(QtWidgets.QLineEdit.Password)
                self.senha.setObjectName("senha")
                self.label_3 = QtWidgets.QLabel(self.frame)
                self.label_3.setGeometry(QtCore.QRect(55, 200, 72, 19))
                self.label_3.setStyleSheet("color: #fff;")
                self.label_3.setObjectName("label_3")
                self.checkBox = QtWidgets.QCheckBox(self.frame)
                self.checkBox.setGeometry(QtCore.QRect(175, 260, 131, 16))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.checkBox.setFont(font)
                self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.checkBox.setAutoFillBackground(False)
                self.checkBox.setStyleSheet("color: #fff;")
                self.checkBox.setObjectName("checkBox")
                self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
                self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
                MainWindow.setCentralWidget(self.centralwidget)

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
                MainWindow.setWindowTitle(_translate("MainWindow", "Criar Conta"))
                self.Titulo.setText(_translate("MainWindow", "Criar Conta "))
                self.btn_criar.setText(_translate("MainWindow", "Criar"))
                self.label_2.setText(_translate("MainWindow", "Beast Bank"))
                self.senha.setPlaceholderText(_translate("MainWindow", "senha de 6 digitos..."))
                self.label_3.setText(_translate("MainWindow", "Senha:"))
                self.checkBox.setText(_translate("MainWindow", "mostrar senha"))
