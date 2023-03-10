from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
        """
        Este é o painel de cadastro do usuário no sistema do banco.

        ...

        Attributes
        ----------
        MainWindow : QMainWindow
                Janela principal do painel de cadastro.
        
        Methods
        -------
        setupUi(MainWindow):
                Configura a janela principal do painel de cadastro.
        retranslateUi(MainWindow):
                Traduz os textos da janela principal do painel de cadastro.
        """
        def setupUi(self, MainWindow):
                """
                Este método configura a janela principal do painel de cadastro.

                Parameters
                ----------
                MainWindow : QMainWindow
                        Janela principal do painel de cadastro.
                
                Returns
                -------
                None
                """
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1366, 768)
                MainWindow.setStyleSheet("background-color: #498f97;")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout.setObjectName("gridLayout")
                self.frame_3 = QtWidgets.QFrame(self.centralwidget)
                self.frame_3.setStyleSheet("border: 0px")
                self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_3.setObjectName("frame_3")
                self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.label_9 = QtWidgets.QLabel(self.frame_3)
                self.label_9.setMaximumSize(QtCore.QSize(16777215, 600))
                font = QtGui.QFont()
                font.setFamily("Suruma")
                font.setPointSize(44)
                self.label_9.setFont(font)
                self.label_9.setStyleSheet("border: 0px")
                self.label_9.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
                self.label_9.setObjectName("label_9")
                self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
                self.label_8 = QtWidgets.QLabel(self.frame_3)
                self.label_8.setMaximumSize(QtCore.QSize(16777215, 300))
                font = QtGui.QFont()
                font.setFamily("Fira Code Light")
                font.setPointSize(14)
                self.label_8.setFont(font)
                self.label_8.setStyleSheet("color:  #fff;")
                self.label_8.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
                self.label_8.setObjectName("label_8")
                self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
                self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 1)
                self.frame_4 = QtWidgets.QFrame(self.centralwidget)
                self.frame_4.setMaximumSize(QtCore.QSize(16777215, 40))
                self.frame_4.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.frame_4.setStyleSheet("border: 0px")
                self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_4.setObjectName("frame_4")
                self.img = QtWidgets.QLabel(self.frame_4)
                self.img.setGeometry(QtCore.QRect(40, 0, 40, 40))
                self.img.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.img.setStyleSheet("background-color: rgb(243, 243, 243);\n"
        "border-radius: 20px;")
                self.img.setText("")
                self.img.setAlignment(QtCore.Qt.AlignCenter)
                self.img.setObjectName("img")
                self.voltar = QtWidgets.QPushButton(self.frame_4)
                self.voltar.setGeometry(QtCore.QRect(40, 0, 40, 40))
                self.voltar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.voltar.setStyleSheet("background-color: rgba(200, 200, 200, 51);\n"
        "border-radius: 20px;\n"
        "")
                self.voltar.setText("")
                self.voltar.setObjectName("voltar")
                self.gridLayout.addWidget(self.frame_4, 1, 0, 1, 1)
                self.frame_2 = QtWidgets.QFrame(self.centralwidget)
                self.frame_2.setStyleSheet("border: 0px")
                self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_2.setObjectName("frame_2")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.frame = QtWidgets.QFrame(self.frame_2)
                self.frame.setMaximumSize(QtCore.QSize(361, 540))
                self.frame.setStyleSheet("background-color: #156068;\n"
        "border-radius: 15px;\n"
        "")
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame")
                self.Titulo = QtWidgets.QLabel(self.frame)
                self.Titulo.setGeometry(QtCore.QRect(100, 40, 161, 51))
                font = QtGui.QFont()
                font.setPointSize(29)
                font.setBold(False)
                font.setWeight(50)
                self.Titulo.setFont(font)
                self.Titulo.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.Titulo.setStyleSheet("color: #fff;\n"
        "font-size: 26;")
                self.Titulo.setAlignment(QtCore.Qt.AlignCenter)
                self.Titulo.setObjectName("Titulo")
                self.nome = QtWidgets.QLineEdit(self.frame)
                self.nome.setGeometry(QtCore.QRect(50, 120, 261, 35))
                self.nome.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.nome.setStyleSheet("QLineEdit{\n"
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
                self.nome.setObjectName("nome")
                self.btn_cadastro = QtWidgets.QPushButton(self.frame)
                self.btn_cadastro.setGeometry(QtCore.QRect(50, 430, 261, 35))
                self.btn_cadastro.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_cadastro.setStyleSheet("QPushButton {\n"
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
                self.btn_cadastro.setObjectName("btn_cadastro")
                self.label = QtWidgets.QLabel(self.frame)
                self.label.setGeometry(QtCore.QRect(105, 470, 115, 19))
                font = QtGui.QFont()
                font.setPointSize(9)
                self.label.setFont(font)
                self.label.setStyleSheet("color: #fff;")
                self.label.setObjectName("label")
                self.btn_login = QtWidgets.QPushButton(self.frame)
                self.btn_login.setGeometry(QtCore.QRect(220, 470, 41, 20))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setUnderline(True)
                self.btn_login.setFont(font)
                self.btn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_login.setStyleSheet("color: #000;")
                self.btn_login.setObjectName("btn_login")
                self.label_2 = QtWidgets.QLabel(self.frame)
                self.label_2.setGeometry(QtCore.QRect(110, 10, 141, 31))
                font = QtGui.QFont()
                font.setFamily("Sawasdee")
                font.setPointSize(20)
                self.label_2.setFont(font)
                self.label_2.setStyleSheet("color: #7cbec6;")
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.cpf = QtWidgets.QLineEdit(self.frame)
                self.cpf.setGeometry(QtCore.QRect(50, 180, 261, 35))
                self.cpf.setStyleSheet("QLineEdit{\n"
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
                self.cpf.setObjectName("cpf")
                self.email = QtWidgets.QLineEdit(self.frame)
                self.email.setGeometry(QtCore.QRect(50, 300, 261, 35))
                self.email.setStyleSheet("QLineEdit{\n"
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
                self.email.setText("")
                self.email.setObjectName("email")
                self.senha = QtWidgets.QLineEdit(self.frame)
                self.senha.setGeometry(QtCore.QRect(50, 360, 261, 35))
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
                self.senha.setText("")
                self.senha.setEchoMode(QtWidgets.QLineEdit.Password)
                self.senha.setObjectName("senha")
                self.label_3 = QtWidgets.QLabel(self.frame)
                self.label_3.setGeometry(QtCore.QRect(55, 220, 151, 20))
                font = QtGui.QFont()
                font.setPointSize(12)
                self.label_3.setFont(font)
                self.label_3.setStyleSheet("color: #fff;")
                self.label_3.setObjectName("label_3")
                self.checkBox = QtWidgets.QCheckBox(self.frame)
                self.checkBox.setGeometry(QtCore.QRect(180, 396, 131, 16))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.checkBox.setFont(font)
                self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.checkBox.setAutoFillBackground(False)
                self.checkBox.setStyleSheet("color: #fff;")
                self.checkBox.setObjectName("checkBox")
                self.label_4 = QtWidgets.QLabel(self.frame)
                self.label_4.setGeometry(QtCore.QRect(55, 340, 72, 19))
                self.label_4.setStyleSheet("color: #fff;")
                self.label_4.setObjectName("label_4")
                self.label_5 = QtWidgets.QLabel(self.frame)
                self.label_5.setGeometry(QtCore.QRect(55, 280, 72, 19))
                self.label_5.setStyleSheet("color: #fff;")
                self.label_5.setObjectName("label_5")
                self.label_6 = QtWidgets.QLabel(self.frame)
                self.label_6.setGeometry(QtCore.QRect(55, 160, 72, 19))
                self.label_6.setStyleSheet("color: #fff;")
                self.label_6.setObjectName("label_6")
                self.label_7 = QtWidgets.QLabel(self.frame)
                self.label_7.setGeometry(QtCore.QRect(55, 100, 131, 19))
                self.label_7.setStyleSheet("color: #fff;")
                self.label_7.setObjectName("label_7")
                self.frame_5 = QtWidgets.QFrame(self.frame)
                self.frame_5.setGeometry(QtCore.QRect(50, 240, 261, 35))
                self.frame_5.setStyleSheet("border-radius: 17px;\n"
        "background-color: #0aabba;")
                self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_5.setObjectName("frame_5")
                self.nascimento = QtWidgets.QDateEdit(self.frame_5)
                self.nascimento.setGeometry(QtCore.QRect(0, 0, 261, 35))
                self.nascimento.setStyleSheet("QDateEdit{\n"
        "    background-color: #fff;\n"
        "    border-radius: 5px;\n"
        "    padding-left: 5px;\n"
        "    border-radius: 17px;\n"
        "    border: 2px solid #498f97;\n"
        "}\n"
        "\n"
        "QDateEdit:focus{\n"
        "    background-color: #fff;\n"
        "    border: 2px ridge rgb(3, 151, 136)    \n"
        "}")
                self.nascimento.setAlignment(QtCore.Qt.AlignCenter)
                self.nascimento.setMinimumDate(QtCore.QDate(1752, 9, 14))
                self.nascimento.setCalendarPopup(True)
                self.nascimento.setDate(QtCore.QDate(2000, 1, 1))
                self.nascimento.setObjectName("nascimento")
                self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
                self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)
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
                MainWindow.setWindowTitle(_translate("MainWindow", "Cadastro"))
                self.label_9.setText(_translate("MainWindow", "Beast Bank"))
                self.label_8.setText(_translate("MainWindow", "Junte-se as feras dos gastos"))
                self.Titulo.setText(_translate("MainWindow", "Cadastro"))
                self.nome.setPlaceholderText(_translate("MainWindow", "ex: João da Silva"))
                self.btn_cadastro.setText(_translate("MainWindow", "Cadastrar"))
                self.label.setText(_translate("MainWindow", "Já possui uma conta?"))
                self.btn_login.setText(_translate("MainWindow", "Login"))
                self.label_2.setText(_translate("MainWindow", "Beast Bank"))
                self.cpf.setPlaceholderText(_translate("MainWindow", "apenas números"))
                self.email.setPlaceholderText(_translate("MainWindow", "ex: joaodasilva@gmail.com"))
                self.senha.setPlaceholderText(_translate("MainWindow", "ex: 12345678"))
                self.label_3.setText(_translate("MainWindow", "Data de nascimento:"))
                self.checkBox.setText(_translate("MainWindow", "mostrar senha"))
                self.label_4.setText(_translate("MainWindow", "Senha:"))
                self.label_5.setText(_translate("MainWindow", "E-mail:"))
                self.label_6.setText(_translate("MainWindow", "CPF:"))
                self.label_7.setText(_translate("MainWindow", "Nome completo:"))
