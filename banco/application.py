from PyQt5                    import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets          import QMessageBox, QMainWindow
from screens.login_screen     import Ui_MainWindow as TelaDeLogin
from screens.cadastro_screen  import Ui_MainWindow as TelaDeCadastro
from screens.user_painel      import Ui_MainWindow as TelaDoUsuario
from screens.account_painel   import Ui_MainWindow as TelaDasContas
from screens.criar_conta      import Ui_MainWindow as TelaDeCriarContas
from screens.extrato          import Ui_MainWindow as TelaDeExtrato
from screens.deposito_e_saque import Ui_MainWindow as TelaDeDepositoESaque
from screens.transferencia    import Ui_MainWindow as TelaDeTransferencia
from bibs.sgbd                import login, add_cliente, create_conta_corrente, create_conta_poupanca, deposito_conta_corrente, deposito_conta_poupanca, get_transacoes, saque_conta_corrente, saque_conta_poupanca, busca_conta_por_cpf, valida_senha_conta_corrente, valida_senha_conta_poupanca
from PIL                      import Image  
import os 


class Main(QMainWindow, TelaDeLogin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.email.setText("moreirapassosj@gmail.com")
        self.senha.setText("12345678")
        self.pushButton.clicked.connect(lambda: self.logIn(self,self))
        self.pushButton_2.clicked.connect(lambda: self.openCadastro(self))
        self.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.checkBox, self.senha))
        img = Image.open("./icons/exit.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.img.setPixmap(img)
        self.voltar.clicked.connect(lambda: self.close())
        
    """
        Métodos de criação de e abertura de janelas
    """
    def openLogin(self, MainWindow=None):
        self.window = QtWidgets.QMainWindow()
        self.login_screen = TelaDeLogin()
        self.login_screen.setupUi(self.window)
        self.login_screen.pushButton.clicked.connect(lambda: self.logIn(self.login_screen, self.window))
        self.login_screen.pushButton_2.clicked.connect(lambda: self.openCadastro(self.window))
        self.login_screen.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.login_screen.checkBox, self.login_screen.senha))
        img = Image.open("./icons/exit.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.login_screen.img.setPixmap(img)
        self.login_screen.voltar.clicked.connect(lambda: self.window.close())
        self.window.show()
        if MainWindow:
            MainWindow.close()
                    
    def openCadastro(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.cadastro_screen = TelaDeCadastro()
        self.cadastro_screen.setupUi(self.window)
        self.cadastro_screen.btn_cadastro.clicked.connect(lambda: self.cadastrar(self.cadastro_screen))
        self.cadastro_screen.btn_login.clicked.connect(lambda: self.openLogin(self.window))
        self.cadastro_screen.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.cadastro_screen.checkBox, self.cadastro_screen.senha))
        img = Image.open("./icons/exit.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.cadastro_screen.img.setPixmap(img)
        self.cadastro_screen.voltar.clicked.connect(lambda: self.window.close())
        self.window.show()
        MainWindow.close()

    def openPainel(self, MainWindow, janela, user):
        self.window = QtWidgets.QMainWindow()
        self.user_screen = TelaDoUsuario()
        self.user_screen.setupUi(self.window)
        self.user_screen.label.setText(f"Bem-vindo(a), {user.nome.split()[0]}!")
        self.user_screen.pushButton_2.clicked.connect(lambda: self.openCriadorDeConta(self.window, user, "corrente") if "cc" not in user.contas.keys() else self.openContas(self.window,user, user.contas['cc'], "cc"))
        self.user_screen.pushButton_3.clicked.connect(lambda: self.openCriadorDeConta(self.window, user, "poupanca") if "cp" not in user.contas.keys() else self.openContas(self.window, user, user.contas['cp'], "cp"))
        self.user_screen.pushButton_5.clicked.connect(lambda: self.openLogin(self.window))
        self.user_screen.pushButton_2.setText("Criar conta corrente" if "cc" not in user.contas.keys() else "Conta corrente")
        self.user_screen.pushButton_3.setText("Criar conta poupança" if "cp" not in user.contas.keys() else "Conta poupança")
        self.window.show()
        MainWindow.close()

    def openCriadorDeConta(self,MainWindow, user, tipo):
        self.window = QtWidgets.QMainWindow()
        self.criador_screen = TelaDeCriarContas()
        self.criador_screen.setupUi(self.window)
        self.criador_screen.btn_criar.clicked.connect(lambda: self.criarContaCorrente(self.window, self.criador_screen, user) if tipo == "corrente" else self.criarContaPoupanca(self.window, self.criador_screen, user))
        img = Image.open("./icons/back.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.criador_screen.img.setPixmap(img)
        self.criador_screen.voltar.clicked.connect(lambda: self.openPainel(self.window, self.criador_screen, user))
        self.window.show()
        MainWindow.close()

    def openContas(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.contas_screen = TelaDasContas()
        self.contas_screen.setupUi(self.window)
        self.contas_screen.tipo.setText("Conta "+ "Corrente" if tipo == "cc" else "Poupança")
        self.contas_screen.numero.setText("nº "+str(conta.numero))
        self.contas_screen.saldo.setText(f"Saldo : R$ {conta.saldo:.2f}".replace(".",","))
        self.contas_screen.checkBox.stateChanged.connect(lambda: self.mostraSaldo(self.contas_screen.checkBox,self.contas_screen.saldo, conta.saldo))
        self.contas_screen.deposito.clicked.connect(lambda: self.openDeposito(self.window, user, conta, tipo))
        img_dep = QtGui.QPixmap("./icons/saque.png", "0", QtCore.Qt.AvoidDither|QtCore.Qt.ThresholdDither|QtCore.Qt.ThresholdAlphaDither)
        self.contas_screen.img_dep.setPixmap(img_dep)
        self.contas_screen.saque.clicked.connect(lambda: self.openSaque(self.window, user, conta, tipo))
        img_saque = QtGui.QPixmap("./icons/saque.png", "0", QtCore.Qt.AvoidDither|QtCore.Qt.ThresholdDither|QtCore.Qt.ThresholdAlphaDither)
        self.contas_screen.img_saque.setPixmap(img_saque)
        self.contas_screen.transferencia.clicked.connect(lambda: self.openTransferencia(self.window, user, conta, tipo))
        img_transf = QtGui.QPixmap("./icons/transferencia.png", "0", QtCore.Qt.AvoidDither|QtCore.Qt.ThresholdDither|QtCore.Qt.ThresholdAlphaDither)
        self.contas_screen.img_transf.setPixmap(img_transf)
        self.contas_screen.extrato.clicked.connect(lambda: self.openExtrato(self.window, user, conta, tipo))
        img_extrato = QtGui.QPixmap("./icons/historico.png", "0", QtCore.Qt.AvoidDither|QtCore.Qt.ThresholdDither|QtCore.Qt.ThresholdAlphaDither)
        self.contas_screen.img_extrato.setPixmap(img_extrato)
        self.contas_screen.btn_sair.clicked.connect(lambda: self.openPainel(self.window, None, user))
        MainWindow.close()
        self.window.show()

    def openDeposito(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Depósito")
        self.deposito_screen = TelaDeDepositoESaque()
        self.deposito_screen.setupUi(self.window)
        self.deposito_screen.operacao.setText("Depósito")
        self.deposito_screen.btn_confirma.clicked.connect(lambda: self.depositar(self.window, user, self.deposito_screen.valor.text(), conta, tipo, self.deposito_screen.senha.text()))
        self.deposito_screen.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.deposito_screen.checkBox, self.deposito_screen.senha))
        self.deposito_screen.voltar.clicked.connect(lambda: self.openContas(self.window, user, conta, tipo))
        img = Image.open("./icons/back.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.deposito_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()
    
    def openSaque(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Saque")
        self.saque_screen = TelaDeDepositoESaque()
        self.saque_screen.setupUi(self.window)
        self.saque_screen.operacao.setText("Saque")
        self.saque_screen.btn_confirma.clicked.connect(lambda: self.sacar(self.window, user, self.saque_screen.valor.text(), conta, tipo, self.saque_screen.senha.text()))
        self.saque_screen.voltar.clicked.connect(lambda: self.openContas(self.window, user, conta, tipo))
        self.saque_screen.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.saque_screen.checkBox, self.saque_screen.senha))
        img = Image.open("./icons/back.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.saque_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()

        
    def openTransferencia(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.transferencia_screen = TelaDeTransferencia()
        self.transferencia_screen.setupUi(self.window)
        self.transferencia_screen.cpf.textChanged.connect(lambda: self.atualizaContas(user,tipo,self.transferencia_screen.frame,self.transferencia_screen.cpf,self.transferencia_screen.comboBox_2))
        self.transferencia_screen.cpf.setFocus()
        self.transferencia_screen.btn_confirma.clicked.connect(lambda: self.transferir(self.window,user, self.transferencia_screen.valor.text(),conta,self.transferencia_screen.cpf.text(),self.transferencia_screen.comboBox_2.currentText(), self.transferencia_screen.senha.text()))
        self.transferencia_screen.checkBox.stateChanged.connect(lambda: self.mostraSenha(self.transferencia_screen.checkBox, self.transferencia_screen.senha))
        self.transferencia_screen.voltar.clicked.connect(lambda: self.openContas(self.window, user, conta, tipo))
        img = Image.open("./icons/back.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.transferencia_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()
    
    def openExtrato(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.extrato_screen = TelaDeExtrato()
        self.extrato_screen.setupUi(self.window)
        historico = get_transacoes(conta.id, tipo)
        height = 2
        labels = []
        horizontal = []
        vertical = []
        if len(historico) > 0:
            line = QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
            # line.setFrameShadow(QtWidgets.QFrame.Plain)
            line.setLineWidth(5)
            line.setMidLineWidth(2)
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setObjectName("line")
            self.extrato_screen.gridLayout.addWidget(line, 1, 0, 1, 8)
            label_6 = QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
            label_6.setStyleSheet("color: #fff")
            label_6.setLineWidth(2)
            label_6.setObjectName("label_6")
            label_6.setText("Data")
            self.extrato_screen.gridLayout.addWidget(label_6, 0, 0, 1, 2)
            line_2 = QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
            line_2.setLineWidth(5)
            line_2.setMidLineWidth(5)
            line_2.setFrameShape(QtWidgets.QFrame.VLine)
            line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_2.setObjectName("line_2")
            self.extrato_screen.gridLayout.addWidget(line_2, 0, 2, 1, 1)
            label_2 = QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
            label_2.setStyleSheet("color: #fff;")
            label_2.setLineWidth(2)
            label_2.setObjectName("label_2")
            label_2.setText("Tipo")
            self.extrato_screen.gridLayout.addWidget(label_2, 0, 3, 1, 2)
            label_3 = QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
            label_3.setEnabled(True)
            label_3.setStyleSheet("color: #fff;")
            label_3.setLineWidth(2)
            label_3.setAlignment(QtCore.Qt.AlignCenter)
            label_3.setObjectName("label_3")
            label_3.setText("Valor")
            self.extrato_screen.gridLayout.addWidget(label_3, 0, 6, 1, 2)
            line_3 = QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
            line_3.setLineWidth(5)
            line_3.setMidLineWidth(5)
            line_3.setFrameShape(QtWidgets.QFrame.VLine)
            line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_3.setObjectName("line_3")
            self.extrato_screen.gridLayout.addWidget(line_3, 0, 5, 1, 1)
            self.extrato_screen.scrollArea.setWidget(self.extrato_screen.scrollAreaWidgetContents)
            for transacao in historico:
                momento = str(transacao[1]).replace("-", "/")
                operacao = transacao[2]
                valor = transacao[3]
                
                labels.append(QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents))
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 0, 1, 2)
                labels[-1].setText(momento)
                labels[-1].setStyleSheet("color: #fff;\n")
                
                vertical.append(QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents))
                vertical[-1].setFrameShape(QtWidgets.QFrame.VLine)
                vertical[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(vertical[-1], height, 2, 1, 1)
                
                labels.append(QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents))
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 3, 1, 2)
                labels[-1].setText(operacao)
                labels[-1].setStyleSheet("color: #fff;\n")
                
                vertical.append(QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents))
                vertical[-1].setFrameShape(QtWidgets.QFrame.VLine)
                vertical[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(vertical[-1], height, 5, 1, 1)
                
                labels.append(QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents))
                labels[-1].setAlignment(QtCore.Qt.AlignCenter)
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 6, 1, 2)
                labels[-1].setText(f"R$ {valor:.2f}".replace(".", ","))
                labels[-1].setStyleSheet("color: #fff;\n")
                
                horizontal.append(QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents))
                horizontal[-1].setFrameShape(QtWidgets.QFrame.HLine)
                horizontal[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(horizontal[-1], height+1, 0, 1, 8)
                
                height += 2
        else:
            label = QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
            label.setStyleSheet("color: #fff;\n""font: 75 14pt \"MS Shell Dlg 2\";")
            label.setLineWidth(2)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName("label")
            label.setText("Essa conta não possui nenhuma transação!")
            self.extrato_screen.gridLayout.addWidget(label, 0, 0, 1, 8)
        self.extrato_screen.voltar.clicked.connect(lambda: self.openContas(self.window, user, conta, tipo))
        img = Image.open("./icons/back.png")
        img = img.resize((30,30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.extrato_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()
        
    """
        Métodos de execução dos butões das telas
    """
    def logIn(self, janela, MainWindow=None):
        email = janela.email.text()
        senha = janela.senha.text()
        if email == "" or senha == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
        else:
            operacao, user = login(email, senha)
            if operacao:
                if MainWindow:
                    MainWindow.close()
                self.openPainel(MainWindow, janela, user)
            else:
                QMessageBox.warning(None, "Erro", "Usuário ou senha incorretos!")

               
    def criarContaCorrente(self, MainWindow, janela, user):
        senha = janela.senha.text()
        if len(senha) != 6:
            QMessageBox.warning(None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if senha == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            cc = create_conta_corrente(user.id, senha)
            user.add_cc(cc)
            self.openPainel(MainWindow, janela, user)
    
    def criarContaPoupanca(self, MainWindow, janela, user):
        senha = janela.senha.text()
        if len(senha) != 6:
            QMessageBox.warning(None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if senha == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            cp = create_conta_poupanca(user.id, senha)
            user.add_cp(cp)
            self.openPainel(MainWindow,janela, user)
            
    def transferir(self, MainWindow, user, valor, conta, cpf_destino, tipo, senha):
        tipo_origem = None
        try:
            l = conta.limite
            tipo_origem = "cc"
        except:
            tipo_origem = "cp"
        cc = busca_conta_por_cpf(cpf_destino, "cc")
        cp = busca_conta_por_cpf(cpf_destino, "cp")
        if cpf_destino == "" or valor == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        try:
            valor = float(valor)
        except:
            QMessageBox.warning(None, "Erro", "Valor inválido!")
        
        if tipo_origem == "cc":
            if not valida_senha_conta_corrente(conta.id, senha):
                QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                saque_conta_corrente(conta.id, conta.numero, valor, True)
                conta.saca(valor)
                try:
                    if tipo == "Conta Corrente":
                        try:
                            deposito_conta_corrente(cc.id, cc.numero, valor, True)
                            QMessageBox.information(None, "Sucesso", "Transferência concluida!")
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except Exception as E:
                            deposito_conta_corrente(conta.id, conta.numero, valor, True)
                            QMessageBox.warning(None, "Erro", str(E))
                            return
                    else:
                        try:
                            deposito_conta_poupanca(cp.id, cp.numero, valor, True)
                            QMessageBox.information(None, "Sucesso", "Transferência concluida!")
                            new_cp = busca_conta_por_cpf(user.cpf, "cp")
                            user.add_cp(new_cp)
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except:
                            deposito_conta_corrente(conta.id, conta.numero, valor, True)
                            QMessageBox.warning(None, "Erro", "Transação não concluida, valor estornado!")
                            return
                except:
                    QMessageBox.warning(None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                QMessageBox.warning(None, "Erro", str(E))
                return
            
        if tipo_origem == "cp":
            if not valida_senha_conta_poupanca(conta.id, senha):
                QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                saque_conta_poupanca(conta.id, conta.numero, valor, True)
                conta.saca(valor)
                try:
                    if tipo == "Conta Corrente":
                        try:
                            deposito_conta_corrente(cc.id, cc.numero, valor, True)
                            QMessageBox.information(None, "Sucesso", "Transferência concluida!")
                            new_cc = busca_conta_por_cpf(user.cpf, "cc")
                            user.add_cc(new_cc)
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except:
                            deposito_conta_poupanca(conta.id, conta.numero, valor, True)
                            conta.deposita(valor)
                            QMessageBox.warning(None, "Erro", "Transação não concluida, valor estornado!")
                            return
                    else:
                        try:
                            deposito_conta_poupanca(cp.id, cp.numero, valor, True)
                            QMessageBox.information(None, "Sucesso", "Transferência concluida!")
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except:
                            deposito_conta_poupanca(conta.id, conta.numero, valor, True)
                            conta.deposita(valor)
                            QMessageBox.warning(None, "Erro", "Transação não concluida, valor estornado!")
                            return
                except:
                    QMessageBox.warning(None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                QMessageBox.warning(None, "Erro", str(E))
                return
        
    def depositar(self, MainWindow,user, valor, conta, tipo, senha):
        try:
            valor = float(valor)
        except:
            QMessageBox.warning(None, "Erro", "Valor inválido!")
        if valor == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
        else:
            if tipo == "cc":
                if not valida_senha_conta_corrente(conta.id, senha):
                    QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    deposito_conta_corrente(conta.id, conta.numero, valor)
                    conta.deposita(valor)
                    QMessageBox.information(None, "Sucesso", "Depósito realizado com sucesso!")
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QMessageBox.warning(None, "Erro", str(E))
            if tipo == "cp":
                if not valida_senha_conta_poupanca(conta.id, senha):
                    QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    deposito_conta_poupanca(conta.id, conta.numero, valor)
                    conta.deposita(valor)
                    QMessageBox.information(None, "Sucesso", "Depósito realizado com sucesso!")
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QMessageBox.warning(None, "Erro", str(E))
    
    def sacar(self, MainWindow, user, valor, conta, tipo, senha):
        try:
            valor = float(valor)
        except:
            QMessageBox.warning(None, "Erro", "Valor inválido!")
        if valor == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
        else:
            if tipo == "cc":
                if not valida_senha_conta_corrente(conta.id, senha):
                    QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    saque_conta_corrente(conta.id, conta.numero, valor)
                    conta.saca(valor)
                    QMessageBox.information(None, "Sucesso", "Saque realizado com sucesso!")
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QMessageBox.warning(None, "Erro", str(E))
            if tipo == "cp":
                if not valida_senha_conta_poupanca(conta.id, senha):
                    QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    saque_conta_poupanca(conta.id, conta.numero, valor)
                    conta.saca(valor)
                    QMessageBox.information(None, "Sucesso", "Saque realizado com sucesso!")
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QMessageBox.warning(None, "Erro", str(E))
    
    def cadastrar(self, MainWindow):
        infos = self.getInfos(MainWindow)
        if infos[0] == "" or infos[1] == "" or infos[2] == "" or infos[3] == "" or infos[4] == "":
            QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        if len(infos[4]) < 8:
            QMessageBox.warning(None, "Erro", "Senha muito curta!")
            return
        if len(infos[4] > 45):
            QMessageBox.warning(None, "Erro", "Senha muito comprida!")
            return
        try:
            add_cliente(infos[0], infos[1], infos[2], infos[3], infos[4])
            QMessageBox.about(None, "Sucesso", "Cadastro realizado com sucesso!")
        except Exception as E:
            QMessageBox.warning(None, "Erro", str(E))
            return
        
    """Métodos auxiliares"""
    
    @staticmethod
    def mostraSaldo(state, label, saldo):
        if state.isChecked():
            label.setText(f"Saldo : R$ {saldo:.2f}".replace(".", ","))
        else:
            label.setText(f"Saldo : R$ {'*' * len(str(saldo))}".replace(".", ","))     
    
    @staticmethod
    def mostraSenha(check, senha):
        if check.isChecked():
            senha.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            senha.setEchoMode(QtWidgets.QLineEdit.Password)
    @staticmethod

    def convertDate(date):
        date = date.split("/")
        return f"{date[2]}-{date[1]}-{date[0]}"
    
    @staticmethod
    def atualizaContas(user, tipo, janela, cpf, select):
        cc = busca_conta_por_cpf(cpf.text(), "cc")
        cp = busca_conta_por_cpf(cpf.text(), "cp")
        select.clear()
        if user.cpf == cpf.text():
            if tipo == "cc":
                if cp:
                    select.addItem(f"Conta Poupança - {cp.numero}")
            elif tipo == "cp":
                if cc:
                    select.addItem(f"Conta Corrente - {cc.numero}")
        else:
            if cc:
                select.addItem(f"Conta Corrente - {cc.numero}")
            if cp:
                select.addItem(f"Conta Poupança - {cp.numero}")           

    
    def getInfos(self, janela):
        nome = janela.nome.text()
        cpf = janela.cpf.text()
        email = janela.email.text()
        senha = janela.senha.text()
        nascimento = self.convertDate(janela.nascimento.text())
        return nome, cpf, nascimento, email, senha
    

        
        
        