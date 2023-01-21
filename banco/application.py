from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from screens.login_screen import Ui_MainWindow as TelaDeLogin
from screens.cadastro_screen import Ui_MainWindow as TelaDeCadastro
from screens.user_painel import Ui_MainWindow as TelaDoUsuario
from screens.account_painel import Ui_MainWindow as TelaDasContas
from screens.criar_conta import Ui_MainWindow as TelaDeCriarContas
from screens.extrato import Ui_MainWindow as TelaDeExtrato
from screens.deposito_e_saque import Ui_MainWindow as TelaDeDepositoESaque
from screens.transferencia import Ui_MainWindow as TelaDeTransferencia
from bibs.consultor_sql import (
    login,
    add_cliente,
    create_conta_corrente,
    create_conta_poupanca,
    deposito_conta_corrente,
    deposito_conta_poupanca,
    get_transacoes,
    get_cliente_id_by_cpf,
    saque_conta_corrente,
    saque_conta_poupanca,
    busca_conta_por_cpf,
    valida_senha_conta_corrente,
    valida_senha_conta_poupanca,
)


class Main(QtWidgets.QMainWindow, TelaDeLogin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.logIn(self, self))
        self.pushButton_2.clicked.connect(lambda: self.openCadastro(self))
        self.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(self.checkBox, self.senha)
        )
        self.email.setText("moreirapassosj@gmail.com")
        self.senha.setText("12345678")
        img = Image.open("./icons/exit.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.img.setPixmap(img)
        self.voltar.clicked.connect(lambda: self.close())

    """
    ------------------------------------------------------------
        Métodos de criação de e abertura de janelas
    ------------------------------------------------------------
    """

    def openLogin(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.login_screen = TelaDeLogin()
        self.login_screen.setupUi(self.window)
        # definindo as ações dos botões
        self.login_screen.pushButton.clicked.connect(
            lambda: self.logIn(self.login_screen, self.window)
        )
        self.login_screen.pushButton_2.clicked.connect(
            lambda: self.openCadastro(self.window)
        )
        self.login_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.login_screen.checkBox, self.login_screen.senha
            )
        )
        # importando incone para o botão de saída
        img = Image.open("./icons/exit.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.login_screen.img.setPixmap(img)
        self.login_screen.voltar.clicked.connect(lambda: self.window.close())
        # mostra a janela de login
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openCadastro(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.cadastro_screen = TelaDeCadastro()
        self.cadastro_screen.setupUi(self.window)
        self.cadastro_screen.nome.setFocus()
        # definição das ações dos botões
        self.cadastro_screen.btn_cadastro.clicked.connect(
            lambda: self.cadastrar(self.cadastro_screen)
        )
        self.cadastro_screen.btn_login.clicked.connect(
            lambda: self.openLogin(self.window)
        )
        self.cadastro_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.cadastro_screen.checkBox, self.cadastro_screen.senha
            )
        )
        # importando incone para o botão de saída
        img = Image.open("./icons/exit.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.cadastro_screen.img.setPixmap(img)
        self.cadastro_screen.voltar.clicked.connect(lambda: self.window.close())
        # mostra a janela de cadastro
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openPainel(self, MainWindow, user):
        self.window = QtWidgets.QMainWindow()
        self.user_screen = TelaDoUsuario()
        self.user_screen.setupUi(self.window)
        # Setando o nome do usuário
        self.user_screen.label.setText(f"Bem-vindo(a), {user.nome.split()[0]}!")
        # definindo as ações dos botões
        self.user_screen.pushButton_2.clicked.connect(
            lambda: self.openCriadorDeConta(self.window, user, "corrente")
            if "cc" not in user.contas.keys()
            else self.openContas(self.window, user, user.contas["cc"], "cc")
        )  # se a conta corrente não existir, abre a tela de criação, se existir, abre a tela de conta
        self.user_screen.pushButton_3.clicked.connect(
            lambda: self.openCriadorDeConta(self.window, user, "poupanca")
            if "cp" not in user.contas.keys()
            else self.openContas(self.window, user, user.contas["cp"], "cp")
        )  # se a conta poupança não existir, abre a tela de criação, se existir, abre a tela de conta
        self.user_screen.pushButton_5.clicked.connect(
            lambda: self.openLogin(self.window)
        )
        # Setando o texto dos botões
        self.user_screen.pushButton_2.setText(
            "Criar conta corrente"
            if "cc" not in user.contas.keys()
            else "Conta corrente"
        )  # se a conta corrente não existir, o texto do botão é "Criar conta corrente", se existir, o texto é "Conta corrente"
        self.user_screen.pushButton_3.setText(
            "Criar conta poupança"
            if "cp" not in user.contas.keys()
            else "Conta poupança"
        )  # se a conta poupança não existir, o texto do botão é "Criar conta poupança", se existir, o texto é "Conta poupança"
        # mostra a janela do usuário
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openCriadorDeConta(self, MainWindow, user, tipo):
        self.window = QtWidgets.QMainWindow()
        self.criador_screen = TelaDeCriarContas()
        self.criador_screen.setupUi(self.window)
        # defini o foco no campo de senha
        self.criador_screen.senha.setFocus()
        # definindo as ações dos botões
        self.criador_screen.btn_criar.clicked.connect(
            lambda: self.criarContaCorrente(self.window, self.criador_screen, user)
            if tipo == "corrente"
            else self.criarContaPoupanca(self.window, self.criador_screen, user)
        )  # se o tipo for "corrente", cria uma conta corrente, se for "poupança", cria uma conta poupança
        self.criador_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.criador_screen.checkBox, self.criador_screen.senha
            )
        )  # se o checkbox for marcado, mostra a senha, se não, esconde
        # importando incone para o botão de voltar
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.criador_screen.img.setPixmap(img)
        self.criador_screen.voltar.clicked.connect(
            lambda: self.openPainel(self.window, user)
        )  # botão de volta para a tela do usuário
        # mostra a janela de criação de conta
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openContas(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.contas_screen = TelaDasContas()
        self.contas_screen.setupUi(self.window)
        # Setando as informações da conta
        self.contas_screen.tipo.setText(
            "Conta " + "Corrente" if tipo == "cc" else "Poupança"
        )
        self.contas_screen.numero.setText("nº " + str(conta.numero))
        self.contas_screen.saldo.setText(
            f"Saldo : R$ {conta.saldo:.2f}".replace(".", ",")
        )
        # Checkbox para mostrar ou esconder o saldo
        self.contas_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSaldo(
                self.contas_screen.checkBox, self.contas_screen.saldo, conta.saldo
            )
        )
        # Botão que abre a tela de depósito
        self.contas_screen.deposito.clicked.connect(
            lambda: self.openDeposito(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de depósito
        img_dep = QtGui.QPixmap(
            "./icons/saque_e_deposito.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.contas_screen.img_dep.setPixmap(img_dep)

        # Botão que abre a tela de saque
        self.contas_screen.saque.clicked.connect(
            lambda: self.openSaque(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de saque
        img_saque = QtGui.QPixmap(
            "./icons/saque_e_deposito.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.contas_screen.img_saque.setPixmap(img_saque)

        # Botão que abre a tela de transferência
        self.contas_screen.transferencia.clicked.connect(
            lambda: self.openTransferencia(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de transferência
        img_transf = QtGui.QPixmap(
            "./icons/transferencia.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.contas_screen.img_transf.setPixmap(img_transf)

        # Botão que abre a tela de extrato
        self.contas_screen.extrato.clicked.connect(
            lambda: self.openExtrato(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de extrato
        img_extrato = QtGui.QPixmap(
            "./icons/historico.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.contas_screen.img_extrato.setPixmap(img_extrato)

        # Botão que fecha a tela da conta e volta para a tela do usuário
        self.contas_screen.btn_sair.clicked.connect(
            lambda: self.openPainel(self.window, user)
        )
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela da conta
        self.window.show()

    def openDeposito(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Depósito")
        self.deposito_screen = TelaDeDepositoESaque()
        self.deposito_screen.setupUi(self.window)
        # Setando o foco no campo de valor
        self.deposito_screen.valor.setFocus()
        self.deposito_screen.operacao.setText("Depósito")
        # Botão de confirmação do depósito
        self.deposito_screen.btn_confirma.clicked.connect(
            lambda: self.depositar(
                self.window,
                user,
                self.deposito_screen.valor.text(),
                conta,
                tipo,
                self.deposito_screen.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.deposito_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.deposito_screen.checkBox, self.deposito_screen.senha
            )
        )
        # Botão de voltar para a tela da conta
        self.deposito_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de voltar
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.deposito_screen.img.setPixmap(img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela do depósito
        self.window.show()

    def openSaque(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Saque")
        self.saque_screen = TelaDeDepositoESaque()
        self.saque_screen.setupUi(self.window)
        # Setando o foco no campo de valor
        self.saque_screen.valor.setFocus()
        self.saque_screen.operacao.setText("Saque")
        # Botão de confirmação do saque
        self.saque_screen.btn_confirma.clicked.connect(
            lambda: self.sacar(
                self.window,
                user,
                self.saque_screen.valor.text(),
                conta,
                tipo,
                self.saque_screen.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.saque_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de voltar
        self.saque_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.saque_screen.checkBox, self.saque_screen.senha
            )
        )
        # Botão de voltar para a tela da conta
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.saque_screen.img.setPixmap(img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela do saque
        self.window.show()

    def openTransferencia(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.transferencia_screen = TelaDeTransferencia()
        self.transferencia_screen.setupUi(self.window)
        # Input que recebe o CPF com um gatilho que busca as contas do usuário x com tal CPF
        self.transferencia_screen.cpf.textChanged.connect(
            lambda: self.atualizaContas(
                user,
                tipo,
                self.transferencia_screen.frame,
                self.transferencia_screen.cpf,
                self.transferencia_screen.comboBox_2,
            )
        )
        # Setando o foco no campo de valor
        self.transferencia_screen.cpf.setFocus()
        # Botão de confirmação da transferência
        self.transferencia_screen.btn_confirma.clicked.connect(
            lambda: self.transferir(
                self.window,
                user,
                self.transferencia_screen.valor.text(),
                conta,
                self.transferencia_screen.cpf.text(),
                self.transferencia_screen.comboBox_2.currentText(),
                self.transferencia_screen.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.transferencia_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.transferencia_screen.checkBox, self.transferencia_screen.senha
            )
        )
        # Botão de voltar para a tela da conta
        self.transferencia_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, conta, tipo)
        )
        # Importando o ícone para o botão de voltar
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.transferencia_screen.img.setPixmap(img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela da transferência
        self.window.show()

    def openExtrato(self, MainWindow, user, conta, tipo):
        self.window = QtWidgets.QMainWindow()
        self.extrato_screen = TelaDeExtrato()
        self.extrato_screen.setupUi(self.window)
        # Pega da data de criação da conta e coloca no formato dd/mm/aaaa
        criacao = str(conta.criacao).split(" ")
        criacao = "/".join(criacao[0].split("-")[::-1]) + " " + criacao[1]
        self.extrato_screen.criacao.setText("Conta criada em " + criacao)
        # Busca no banco de dados as últimas 10 transações da conta
        historico = get_transacoes(conta.id, tipo)
        historico.sort(key=lambda x: x[1], reverse=True)
        historico = historico[:10]
        height = 2
        labels = []
        horizontal = []
        vertical = []
        # Verifica se há transações no histórico. Se houver, cria os labels e adiciona no grid layout
        if len(historico) > 0:
            line = QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
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
            self.extrato_screen.scrollArea.setWidget(
                self.extrato_screen.scrollAreaWidgetContents
            )
            # Para cada transação, cria um label com a data e hora, um label com o tipo de transação e um label com o valor
            # todos os labels ocupa 1 linha e 2 colunas
            for transacao in historico:
                # Pega a data e hora da transação e coloca no formato dd/mm/aaaa hh:mm:ss
                momento = str(transacao[1]).split(" ")
                momento = "/".join(momento[0].split("-")[::-1]) + " " + momento[1]
                # Pega o tipo de transação e o valor
                operacao = transacao[2]
                # Pega o valor da operação
                valor = transacao[3]

                # Criando os labels e linhas
                labels.append(
                    QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
                )
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 0, 1, 2)
                labels[-1].setText(momento)
                labels[-1].setStyleSheet("color: #fff;\n")

                vertical.append(
                    QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
                )
                vertical[-1].setFrameShape(QtWidgets.QFrame.VLine)
                vertical[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(vertical[-1], height, 2, 1, 1)

                labels.append(
                    QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
                )
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 3, 1, 2)
                labels[-1].setText(operacao)
                labels[-1].setStyleSheet("color: #fff;\n")

                vertical.append(
                    QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
                )
                vertical[-1].setFrameShape(QtWidgets.QFrame.VLine)
                vertical[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(vertical[-1], height, 5, 1, 1)

                labels.append(
                    QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
                )
                labels[-1].setAlignment(QtCore.Qt.AlignCenter)
                self.extrato_screen.gridLayout.addWidget(labels[-1], height, 6, 1, 2)
                labels[-1].setText(f"R$ {valor:.2f}".replace(".", ","))
                labels[-1].setStyleSheet("color: #fff;\n")

                horizontal.append(
                    QtWidgets.QFrame(self.extrato_screen.scrollAreaWidgetContents)
                )
                horizontal[-1].setFrameShape(QtWidgets.QFrame.HLine)
                horizontal[-1].setFrameShadow(QtWidgets.QFrame.Sunken)
                self.extrato_screen.gridLayout.addWidget(
                    horizontal[-1], height + 1, 0, 1, 8
                )

                height += 2
        else:
            # Se não houver nenhuma transação, cria um label dizendo que não há transações
            label = QtWidgets.QLabel(self.extrato_screen.scrollAreaWidgetContents)
            label.setStyleSheet("color: #fff;\n" 'font: 75 14pt "MS Shell Dlg 2";')
            label.setLineWidth(2)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName("label")
            label.setText("Essa conta não possui nenhuma transação!")
            self.extrato_screen.gridLayout.addWidget(label, 0, 0, 1, 8)
        # Cria um botão para voltar para a tela de contas
        self.extrato_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, conta, tipo)
        )
        # Importa o ícone de voltar
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.extrato_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()

    """
    ---------------------------------------------------
        Métodos de execução dos butões das telas
    ---------------------------------------------------
    """

    def logIn(self, janela, MainWindow=None):
        email = janela.email.text()
        senha = janela.senha.text()
        if email == "" or senha == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
        else:
            operacao, user = login(email, senha)
            if operacao:
                if MainWindow:
                    MainWindow.close()
                self.openPainel(MainWindow, user)
            else:
                QtWidgets.QMessageBox.warning(
                    None, "Erro", "Usuário ou senha incorretos!"
                )

    def criarContaCorrente(self, MainWindow, janela, user):
        senha = janela.senha.text()
        if len(senha) != 6:
            QtWidgets.QMessageBox.warning(None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if senha == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            cc = create_conta_corrente(user.id, senha)
            user.add_cc(cc)
            self.openPainel(MainWindow, user)

    def criarContaPoupanca(self, MainWindow, janela, user):
        senha = janela.senha.text()
        if len(senha) != 6:
            QtWidgets.QMessageBox.warning(None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if senha == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            cp = create_conta_poupanca(user.id, senha)
            user.add_cp(cp)
            self.openPainel(MainWindow, user)

    def transferir(self, MainWindow, user, valor, conta, cpf_destino, tipo, senha):
        # Inicializando o tipo da conta
        tipo_origem = None
        try:
            # Se na conta existir um limite, então é uma conta corrente
            # Se não, entra no tratamento de erro, pois vai tentar acessar um atributo que não existe e define o tipo como conta poupança
            l = conta.limite
            tipo_origem = "cc"
        except:
            tipo_origem = "cp"
        # Busca a conta de destino no banco de dados através do cpf
        cc = busca_conta_por_cpf(cpf_destino, "cc")
        cp = busca_conta_por_cpf(cpf_destino, "cp")
        # Busca o id do cliente de destino no banco de dados através do cpf
        id_destino = get_cliente_id_by_cpf(cpf_destino)
        # verifica campos vazios
        if cpf_destino == "" or valor == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        try:
            # Verifica se o valor passado é um valor numérico
            valor = float(valor)
        except:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return

        # Verifica se a conta de origem é uma conta corrente
        if tipo_origem == "cc":
            # Faz a validação da senha passada pelo usuário
            if not valida_senha_conta_corrente(conta.id, senha):
                QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                # Vai no banco de dados tentar fazer o saque na conta corrente de origem
                saque_conta_corrente(
                    conta.id,
                    conta.numero,
                    valor,
                    True,
                    id_destino,
                    "cc" if tipo == "Conta Corrente" else "cp",
                )
                conta.saca(valor)
                try:
                    # Vai no banco de dados tentar fazer o depósito na conta de destino
                    # Verifica o tipo da conta de destino
                    if tipo == "Conta Corrente":
                        try:
                            # Tenta fazer o depósito na conta corrente de destino,
                            deposito_conta_corrente(
                                cc.id, cc.numero, valor, True, user.id, tipo_origem
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except Exception as E:
                            # se não conseguir fazer o depósito, faz o estorno na conta de origem
                            deposito_conta_corrente(conta.id, conta.numero, valor)
                            QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                            return
                    else:  # se não for conta corrente, é conta poupança
                        try:
                            # Tenta fazer o depósito na conta poupança de destino
                            deposito_conta_poupanca(
                                cp.id, cp.numero, valor, True, user.id, tipo_origem
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            new_cp = busca_conta_por_cpf(user.cpf, "cp")
                            user.add_cp(new_cp)
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except Exception as E:
                            # Se não conseguir fazer o depósito, faz o estorno na conta de origem
                            deposito_conta_corrente(conta.id, conta.numero, valor)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                except:
                    QtWidgets.QMessageBox.warning(None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                # Se não coseguir fazer o saque.
                QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                return
        # Mesma lógica da conta corrente, só que para conta poupança
        if tipo_origem == "cp":
            if not valida_senha_conta_poupanca(conta.id, senha):
                QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                saque_conta_poupanca(
                    conta.id,
                    conta.numero,
                    valor,
                    True,
                    id_destino,
                    "cc" if tipo == "Conta Corrente" else "cp",
                )
                conta.saca(valor)
                try:
                    if tipo == "Conta Corrente":
                        try:
                            deposito_conta_corrente(
                                cc.id, cc.numero, valor, True, user.id, tipo_origem
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            new_cc = busca_conta_por_cpf(user.cpf, "cc")
                            user.add_cc(new_cc)
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except:
                            deposito_conta_poupanca(conta.id, conta.numero, valor)
                            conta.deposita(valor)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                    else:
                        try:
                            deposito_conta_poupanca(
                                cp.id, cp.numero, valor, True, user.id, tipo_origem
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            self.openContas(MainWindow, user, conta, tipo_origem)
                        except:
                            deposito_conta_poupanca(conta.id, conta.numero, valor)
                            conta.deposita(valor)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                except:
                    QtWidgets.QMessageBox.warning(None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                return

    def depositar(self, MainWindow, user, valor, conta, tipo, senha):
        try:
            # Verifica se o valor passado é um valor númerico
            valor = float(valor)
        except:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return
        # Verifica se campo valor está vazio
        if valor == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            # Verifica o tipo da conta e faz o depósito
            if tipo == "cc":
                # Verifica se a senha está correta
                if not valida_senha_conta_corrente(conta.id, senha):
                    QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    # Faz o depósito
                    deposito_conta_corrente(conta.id, conta.numero, valor)
                    conta.deposita(valor)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Depósito realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    # Se não conseguir fazer o depósito, mostra o erro
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return
            # Mesma lógica da conta corrente, só que para conta poupança
            if tipo == "cp":
                if not valida_senha_conta_poupanca(conta.id, senha):
                    QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    deposito_conta_poupanca(conta.id, conta.numero, valor)
                    conta.deposita(valor)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Depósito realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return

    def sacar(self, MainWindow, user, valor, conta, tipo, senha):
        try:
            # Verifica se o valor passado é um valor numérico
            valor = float(valor)
        except:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return
        # Verifica o campo está vazio
        if valor == "":
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        else:
            # Verifica se o tipo da conta é conta corrente
            if tipo == "cc":
                # Verifica se a senha é válida
                if not valida_senha_conta_corrente(conta.id, senha):
                    QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    # Realiza o saque
                    saque_conta_corrente(conta.id, conta.numero, valor)
                    conta.saca(valor)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Saque realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    # Caso ocorra algum erro, exibe a mensagem de erro
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return
            # Mesma lógica da conta corrente, só que para conta poupança
            if tipo == "cp":
                if not valida_senha_conta_poupanca(conta.id, senha):
                    QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                    return
                try:
                    saque_conta_poupanca(conta.id, conta.numero, valor)
                    conta.saca(valor)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Saque realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, conta, tipo)
                except Exception as E:
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return

    def cadastrar(self, MainWindow):
        infos = self.getInfos(MainWindow)
        if (
            infos[0] == ""
            or infos[1] == ""
            or infos[2] == ""
            or infos[3] == ""
            or infos[4] == ""
        ):
            QtWidgets.QMessageBox.warning(None, "Erro", "Preencha todos os campos!")
            return
        if len(infos[4]) < 8:
            QtWidgets.QMessageBox.warning(None, "Erro", "Senha muito curta!")
            return
        if len(infos[4]) > 45:
            QtWidgets.QMessageBox.warning(None, "Erro", "Senha muito comda!")
            return
        try:
            add_cliente(infos[0], infos[1], infos[2], infos[3], infos[4])
            QtWidgets.QMessageBox.about(
                None, "Sucesso", "Cadastro realizado com sucesso!"
            )
            return
        except Exception as E:
            QtWidgets.QMessageBox.warning(None, "Erro", str(E))
            return

    """
    -----------------------------------------------------
    Métodos auxiliares  
    -----------------------------------------------------
    """

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
