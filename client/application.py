from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from screens.extrato import Ui_MainWindow as TelaDeExtrato
from screens.login_screen import Ui_MainWindow as TelaDeLogin
from screens.user_painel import Ui_MainWindow as TelaDoUsuario
from screens.account_painel import Ui_MainWindow as TelaDasContas
from screens.criar_conta import Ui_MainWindow as TelaDeCriarContas
from screens.cadastro_screen import Ui_MainWindow as TelaDeCadastro
from screens.transferencia import Ui_MainWindow as TelaDeTransferencia
from screens.deposito_e_saque import Ui_MainWindow as TelaDeDepositoESaque
from client import (
    login,
    add_cliente,
    get_transacoes,
    busca_conta_por_cpf,
    saque_conta_corrente,
    saque_conta_poupanca,
    create_conta_corrente,
    create_conta_poupanca,
    get_cliente_id_by_cpf,
    deposito_conta_corrente,
    deposito_conta_poupanca,
    valida_senha_conta_corrente,
    valida_senha_conta_poupanca,
    get_user_by_id
)


class Main(QtWidgets.QMainWindow, TelaDeLogin):
    """
    A classe Main é a classe principal do programa, ela é responsável por gerenciar as janelas do programa e as ações dos botões de cada uma delas.

    A classe Main herda de duas classes, a classe QtWidgets.QMainWindow e a classe TelaDeLogin, a primeira é a classe principal do PyQt5, a segunda é a classe que contém os métodos e atributos da tela de login.

    ...

    Attributes
    ----------
    Muitos atributos são herdados da classe TelaDeLogin, que contém os métodos e atributos da tela de login.

    Methods
    -------
    openLogin(MainWindow):
        Abre a tela de login e fecha a tela anterior.
    openCadastro(MainWindow):
        Abre a tela de cadastro e fecha a tela anterior.
    openPainel(MainWindow, user):
        Abre a tela do usuário e fecha a tela anterior.
    openCriadorDeConta(MainWindow, MainWindow, user, account_type):
        Abre a tela de criação de contas e fecha a tela anterior.
    Continua aqui
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.logIn(self, self))
        self.pushButton_2.clicked.connect(lambda: self.openCadastro(self))
        self.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(self.checkBox, self.senha)
        )
        self.email.setText("test")
        self.senha.setText("12345678")
        exit_icon_img = Image.open("./icons/exit.png")
        exit_icon_img = exit_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        exit_icon_img = QtGui.QPixmap(exit_icon_img.toqpixmap())
        self.img.setPixmap(exit_icon_img)
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
        exit_icon_img = Image.open("./icons/exit.png")
        exit_icon_img = exit_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        exit_icon_img = QtGui.QPixmap(exit_icon_img.toqpixmap())
        self.login_screen.img.setPixmap(exit_icon_img)
        self.login_screen.voltar.clicked.connect(lambda: self.window.close())
        # mostra a janela de login
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openCadastro(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.registration_screen = TelaDeCadastro()
        self.registration_screen.setupUi(self.window)
        self.registration_screen.nome.setFocus()
        # definição das ações dos botões
        self.registration_screen.btn_cadastro.clicked.connect(
            lambda: self.cadastrar(self.registration_screen)
        )
        self.registration_screen.btn_login.clicked.connect(
            lambda: self.openLogin(self.window)
        )
        self.registration_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.registration_screen.checkBox,
                self.registration_screen.senha
            )
        )
        # importando incone para o botão de saída
        exit_icon_img = Image.open("./icons/exit.png")
        exit_icon_img = exit_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        exit_icon_img = QtGui.QPixmap(exit_icon_img.toqpixmap())
        self.registration_screen.img.setPixmap(exit_icon_img)
        self.registration_screen.voltar.clicked.connect(
            lambda: self.window.close())
        # mostra a janela de cadastro
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openPainel(self, MainWindow, user):
        user = get_user_by_id(user.id)
        self.window = QtWidgets.QMainWindow()
        self.user_screen = TelaDoUsuario()
        self.user_screen.setupUi(self.window)
        # Setando o nome do usuário
        self.user_screen.label.setText(
            f"Bem-vindo(a), {user.nome.split()[0]}!")
        # definindo as ações dos botões

        """
        se a conta corrente não existir, abre a tela de criação,
        se existir, abre a tela de conta
         """
        self.user_screen.pushButton_2.clicked.connect(
            lambda: self.openCriadorDeConta(self.window, user, "corrente")
            if "cc" not in user.contas.keys()
            else self.openContas(self.window, user, user.contas["cc"], "cc")
        )
        """
        se a conta poupança não existir, abre a tela de criação,
        se existir, abre a tela de conta
        """
        self.user_screen.pushButton_3.clicked.connect(
            lambda: self.openCriadorDeConta(self.window, user, "poupanca")
            if "cp" not in user.contas.keys()
            else self.openContas(self.window, user, user.contas["cp"], "cp")
        )
        self.user_screen.pushButton_5.clicked.connect(
            lambda: self.openLogin(self.window)
        )
        """
        Setando o texto dos botões
        se a conta corrente não existir, o texto do botão é
        'Criar conta corrente', se existir, o texto é 'Conta corrente'
        """
        self.user_screen.pushButton_2.setText(
            "Criar conta corrente"
            if "cc" not in user.contas.keys()
            else "Conta corrente"
        )
        """
        se a conta poupança não existir, o texto do botão é
        'Criar conta poupança', se existir, o texto é    Conta poupança'
        """
        self.user_screen.pushButton_3.setText(
            "Criar conta poupança"
            if "cp" not in user.contas.keys()
            else "Conta poupança"
        )
        # mostra a janela do usuário
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openCriadorDeConta(self, MainWindow, user, account_type):
        self.window = QtWidgets.QMainWindow()
        self.account_creator_screen = TelaDeCriarContas()
        self.account_creator_screen.setupUi(self.window)
        # defini o foco no campo de senha
        self.account_creator_screen.senha.setFocus()
        # definindo as ações dos botões
        self.account_creator_screen.btn_criar.clicked.connect(
            lambda: self.criarContaCorrente(
                self.window, self.account_creator_screen, user
            )
            if account_type == "corrente"
            else self.criarContaPoupanca(self.window,
                                         self.account_creator_screen,
                                         user
                                         )
        )
        """
        se o tipo for "corrente", cria uma conta corrente,
        se for "poupança", cria uma conta poupança
        """
        self.account_creator_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.account_creator_screen.checkBox,
                self.account_creator_screen.senha
            )
        )  # se o checkbox for marcado, mostra a senha, se não, esconde
        # importando incone para o botão de voltar
        back_icon_img = Image.open("./icons/back.png")
        back_icon_img = back_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        back_icon_img = QtGui.QPixmap(back_icon_img.toqpixmap())
        self.account_creator_screen.img.setPixmap(back_icon_img)
        self.account_creator_screen.voltar.clicked.connect(
            lambda: self.openPainel(self.window, user)
        )  # botão de volta para a tela do usuário
        # mostra a janela de criação de conta
        self.window.show()
        # fecha a janela anterior
        MainWindow.close()

    def openContas(self, MainWindow, user, account, account_type):
        user = get_user_by_id(user.id)
        if account_type == "cc":
            account = user.contas["cc"]
        elif account_type == "cp":
            account = user.contas["cp"]
        self.window = QtWidgets.QMainWindow()
        self.accounts_screen = TelaDasContas()
        self.accounts_screen.setupUi(self.window)
        # Setando as informações da conta
        self.accounts_screen.tipo.setText(
            "Conta " + "Corrente" if account_type == "cc" else "Poupança"
        )
        self.accounts_screen.numero.setText("nº " + str(account.numero))
        self.accounts_screen.saldo.setText(
            f"Saldo : R$ {account.saldo:.2f}".replace(".", ",")
        )
        # Checkbox para mostrar ou esconder o saldo
        self.accounts_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSaldo(
                self.accounts_screen.checkBox,
                self.accounts_screen.saldo,
                account.saldo
            )
        )
        # Botão que abre a tela de depósito
        self.accounts_screen.deposito.clicked.connect(
            lambda: self.openDeposito(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de depósito
        deposit_icon_img = QtGui.QPixmap(
            "./icons/saque_e_deposito.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.accounts_screen.img_dep.setPixmap(deposit_icon_img)

        # Botão que abre a tela de saque
        self.accounts_screen.saque.clicked.connect(
            lambda: self.openSaque(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de saque
        withdraw_icon_img = QtGui.QPixmap(
            "./icons/saque_e_deposito.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.accounts_screen.img_saque.setPixmap(withdraw_icon_img)

        # Botão que abre a tela de transferência
        self.accounts_screen.transferencia.clicked.connect(
            lambda: self.openTransferencia(
                self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de transferência
        tranfer_icon_img = QtGui.QPixmap(
            "./icons/transferencia.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.accounts_screen.img_transf.setPixmap(tranfer_icon_img)

        # Botão que abre a tela de extrato
        self.accounts_screen.extrato.clicked.connect(
            lambda: self.openExtrato(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de extrato
        historic_icon_img = QtGui.QPixmap(
            "./icons/historico.png",
            "0",
            QtCore.Qt.AvoidDither
            | QtCore.Qt.ThresholdDither
            | QtCore.Qt.ThresholdAlphaDither,
        )
        self.accounts_screen.img_extrato.setPixmap(historic_icon_img)

        # Botão que fecha a tela da conta e volta para a tela do usuário
        self.accounts_screen.btn_sair.clicked.connect(
            lambda: self.openPainel(self.window, user)
        )
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela da conta
        self.window.show()

    def openDeposito(self, MainWindow, user, account, account_type):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Depósito")
        self.deposit_screen = TelaDeDepositoESaque()
        self.deposit_screen.setupUi(self.window)
        # Setando o foco no campo de valor
        self.deposit_screen.valor.setFocus()
        self.deposit_screen.operacao.setText("Depósito")
        # Botão de confirmação do depósito
        self.deposit_screen.btn_confirma.clicked.connect(
            lambda: self.depositar(
                self.window,
                user,
                self.deposit_screen.valor.text(),
                account,
                account_type,
                self.deposit_screen.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.deposit_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.deposit_screen.checkBox, self.deposit_screen.senha
            )
        )
        # Botão de voltar para a tela da conta
        self.deposit_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de voltar
        back_icon_img = Image.open("./icons/back.png")
        back_icon_img = back_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        back_icon_img = QtGui.QPixmap(back_icon_img.toqpixmap())
        self.deposit_screen.img.setPixmap(back_icon_img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela do depósito
        self.window.show()

    def openSaque(self, MainWindow, user, account, account_type):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Saque")
        self.withdraw_screnn = TelaDeDepositoESaque()
        self.withdraw_screnn.setupUi(self.window)
        # Setando o foco no campo de valor
        self.withdraw_screnn.valor.setFocus()
        self.withdraw_screnn.operacao.setText("Saque")
        # Botão de confirmação do saque
        self.withdraw_screnn.btn_confirma.clicked.connect(
            lambda: self.sacar(
                self.window,
                user,
                self.withdraw_screnn.valor.text(),
                account,
                account_type,
                self.withdraw_screnn.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.withdraw_screnn.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de voltar
        self.withdraw_screnn.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.withdraw_screnn.checkBox, self.withdraw_screnn.senha
            )
        )
        # Botão de voltar para a tela da conta
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.withdraw_screnn.img.setPixmap(img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela do saque
        self.window.show()

    def openTransferencia(self, MainWindow, user, account, account_type):
        self.window = QtWidgets.QMainWindow()
        self.transfer_screen = TelaDeTransferencia()
        self.transfer_screen.setupUi(self.window)
        """
        Input que recebe o CPF com um gatilho que busca as contas
        do usuário x com tal CPF
        """
        self.transfer_screen.cpf.textChanged.connect(
            lambda: self.atualizaContas(
                user,
                account_type,
                self.transfer_screen.cpf,
                self.transfer_screen.comboBox_2,
            )
        )
        # Setando o foco no campo de valor
        self.transfer_screen.cpf.setFocus()
        # Botão de confirmação da transferência
        self.transfer_screen.btn_confirma.clicked.connect(
            lambda: self.transferir(
                self.window,
                user,
                self.transfer_screen.valor.text(),
                account,
                self.transfer_screen.cpf.text(),
                self.transfer_screen.comboBox_2.currentText(),
                self.transfer_screen.senha.text(),
            )
        )
        # Checkbox para mostrar ou esconder a senha
        self.transfer_screen.checkBox.stateChanged.connect(
            lambda: self.mostraSenha(
                self.transfer_screen.checkBox, self.transfer_screen.senha
            )
        )
        # Botão de voltar para a tela da conta
        self.transfer_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, account, account_type)
        )
        # Importando o ícone para o botão de voltar
        back_icon_img = Image.open("./icons/back.png")
        back_icon_img = back_icon_img.resize(
            (30, 30), Image.Resampling.LANCZOS)
        back_icon_img = QtGui.QPixmap(back_icon_img.toqpixmap())
        self.transfer_screen.img.setPixmap(back_icon_img)
        # fecha a janela anterior
        MainWindow.close()
        # mostra a janela da transferência
        self.window.show()

    def openExtrato(self, MainWindow, user, account, account_type):
        self.window = QtWidgets.QMainWindow()
        self.historic_screen = TelaDeExtrato()
        self.historic_screen.setupUi(self.window)
        # Pega da data de criação da conta e coloca no formato dd/mm/aaaa
        account_data_creation = str(account.criacao).split(" ")
        account_data_creation = (
            "/".join(account_data_creation[0].split("-")[::-1])
            + " "
            + account_data_creation[1]
        )
        self.historic_screen.criacao.setText(
            "Conta criada em " + account_data_creation)
        # Busca no banco de dados as últimas 10 transações da conta
        historic = get_transacoes(account.id, account_type)
        historic.sort(key=lambda x: x[1], reverse=True)
        historic = historic[0:10]
        height = 2
        labels = []
        """
        Verifica se há transações no histórico.
        Se houver, cria os labels e adiciona no grid layout
        """
        if len(historic) > 0:
            label_6 = QtWidgets.QLabel(
                self.historic_screen.scrollAreaWidgetContents)
            label_6.setStyleSheet("color: #fff")
            label_6.setLineWidth(2)
            label_6.setObjectName("label_6")
            label_6.setText("Data")
            self.historic_screen.gridLayout.addWidget(label_6, 0, 0, 2, 2)
            label_2 = QtWidgets.QLabel(
                self.historic_screen.scrollAreaWidgetContents)
            label_2.setStyleSheet("color: #fff;")
            label_2.setLineWidth(2)
            label_2.setObjectName("label_2")
            label_2.setText("Tipo")
            self.historic_screen.gridLayout.addWidget(label_2, 0, 2, 2, 2)
            label_3 = QtWidgets.QLabel(
                self.historic_screen.scrollAreaWidgetContents)
            label_3.setEnabled(True)
            label_3.setStyleSheet("color: #fff;")
            label_3.setLineWidth(2)
            label_3.setAlignment(QtCore.Qt.AlignCenter)
            label_3.setObjectName("label_3")
            label_3.setText("Valor")
            self.historic_screen.gridLayout.addWidget(label_3, 0, 4, 2, 2)
            self.historic_screen.scrollArea.setWidget(
                self.historic_screen.scrollAreaWidgetContents
            )
            """
            Para cada transação, cria um label com a data e hora,
            um label com o tipo de transação e um label com o valor
            todos os labels ocupa 1 linha e 2 colunas
            """
            for transaction in historic:
                """
                Pega a data e hora da transação e coloca no formato:
                                                        dd/mm/aaaa hh:mm:ss
                """
                time = str(transaction[1]).split(" ")
                time = "/".join(time[0].split("-")[::-1]) + " " + time[1]
                # Pega o tipo de transação e o valor
                operation = transaction[2]
                # Pega o valor da operação
                valor = transaction[3]

                # Criando os labels e linhas
                labels.append(
                    QtWidgets.QLabel(
                        self.historic_screen.scrollAreaWidgetContents)
                )
                self.historic_screen.gridLayout.addWidget(
                    labels[-1], height, 0, 1, 2)
                labels[-1].setText(time)
                labels[-1].setStyleSheet("color: #fff;\n")

                labels.append(
                    QtWidgets.QLabel(
                        self.historic_screen.scrollAreaWidgetContents)
                )
                self.historic_screen.gridLayout.addWidget(
                    labels[-1], height, 2, 1, 2)
                labels[-1].setText(operation)
                labels[-1].setStyleSheet("color: #fff;\n")

                labels.append(
                    QtWidgets.QLabel(
                        self.historic_screen.scrollAreaWidgetContents)
                )
                labels[-1].setAlignment(QtCore.Qt.AlignCenter)
                self.historic_screen.gridLayout.addWidget(
                    labels[-1], height, 4, 1, 2)
                labels[-1].setText(f"R$ {valor:.2f}".replace(".", ","))
                labels[-1].setStyleSheet("color: #fff;\n")

                height += 2
        else:
            """
            Se não houver nenhuma transação,
            cria um label dizendo que não há transações
            """
            label = QtWidgets.QLabel(
                self.historic_screen.scrollAreaWidgetContents)
            label.setStyleSheet(
                "color: #fff;\n" 'font: 75 14pt "MS Shell Dlg 2";')
            label.setLineWidth(2)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName("label")
            label.setText("Essa conta não possui nenhuma transação!")
            self.historic_screen.gridLayout.addWidget(label, 0, 0, 1, 8)
        # Cria um botão para voltar para a tela de contas
        self.historic_screen.voltar.clicked.connect(
            lambda: self.openContas(self.window, user, account, account_type)
        )
        # Importa o ícone de voltar
        img = Image.open("./icons/back.png")
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        img = QtGui.QPixmap(img.toqpixmap())
        self.historic_screen.img.setPixmap(img)
        MainWindow.close()
        self.window.show()

    """
    ---------------------------------------------------
        Métodos de execução dos butões das telas
    ---------------------------------------------------
    """

    def logIn(self, inputs_window, MainWindow=None):
        email = inputs_window.email.text()
        password = inputs_window.senha.text()
        if email == "" or password == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
        else:
            operacao, user = login(email, password)
            if operacao:
                if MainWindow:
                    MainWindow.close()
                self.openPainel(MainWindow, user)
            else:
                QtWidgets.QMessageBox.warning(
                    None, "Erro", "Usuário ou senha incorretos!"
                )

    def criarContaCorrente(self, MainWindow, inputs_window, user):
        password = inputs_window.senha.text()
        if len(password) != 6:
            QtWidgets.QMessageBox.warning(
                None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if password == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        else:
            cc = create_conta_corrente(user.id, password)
            user.add_cc(cc)
            self.openPainel(MainWindow, user)

    def criarContaPoupanca(self, MainWindow, inputs_window, user):
        password = inputs_window.senha.text()
        if len(password) != 6:
            QtWidgets.QMessageBox.warning(
                None, "Erro", "A senha deve ter 6 dígitos!")
            return
        if password == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        else:
            cp = create_conta_poupanca(user.id, password)
            user.add_cp(cp)
            self.openPainel(MainWindow, user)

    def transferir(
        self,
        MainWindow,
        user,
        value,
        account,
        target_cpf,
        target_account_type,
        password,
    ):
        target_account_type = target_account_type.split(" - ")[0]
        # Inicializando o tipo da conta
        account_source_type = None
        try:
            """
             Se na conta existir um limite, então é uma conta corrente
             Se não, entra no tratamento de erro, pois vai tentar acessar
             um atributo que não existe e define o tipo como conta poupança
            """
            account.limite = account.limite
            account_source_type = "cc"
        except Exception:
            account_source_type = "cp"
        # Busca a conta de destino no banco de dados através do cpf
        cc = busca_conta_por_cpf(target_cpf, "cc")
        cp = busca_conta_por_cpf(target_cpf, "cp")
        # Busca o id do cliente de destino no banco de dados através do cpf
        target_user_id = get_cliente_id_by_cpf(target_cpf)
        # verifica campos vazios
        if target_cpf == "" or value == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        try:
            # Verifica se o valor passado é um valor numérico
            value = float(value)
        except Exception:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return

        # Verifica se a conta de origem é uma conta corrente
        if account_source_type == "cc":
            # Faz a validação da senha passada pelo usuário
            if not valida_senha_conta_corrente(account.id, password):
                QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                """
                Vai no banco de dados tentar fazer o saque
                na conta corrente de origem
                """
                saque_conta_corrente(
                    account.id,
                    account.numero,
                    value,
                    True,
                    target_user_id,
                    "cc" if target_account_type == "Conta Corrente" else "cp",
                )
                account.saca(value)
                try:
                    """
                    Vai no banco de dados tentar fazer o depósito na conta
                    de destino.
                    """
                    # Verifica o tipo da conta de destino
                    if target_account_type == "Conta Corrente":
                        try:
                            """
                            Tenta fazer o depósito na conta corrente de destino
                            """
                            deposito_conta_corrente(
                                cc.id,
                                cc.numero,
                                value,
                                True,
                                user.id,
                                account_source_type,
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            self.openContas(
                                MainWindow, user, account, account_source_type
                            )
                        except Exception as E:
                            """
                            se não conseguir fazer o depósito,
                            faz o estorno na conta de origem
                            """
                            deposito_conta_corrente(
                                account.id, account.numero, value)
                            QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                            return
                    else:  # se não for conta corrente, é conta poupança
                        try:
                            """
                            Tenta fazer o depósito na conta poupança de destino
                            """
                            deposito_conta_poupanca(
                                cp.id,
                                cp.numero,
                                value,
                                True,
                                user.id,
                                account_source_type,
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            new_cp = busca_conta_por_cpf(user.cpf, "cp")
                            user.add_cp(new_cp)
                            self.openContas(
                                MainWindow, user, account, account_source_type
                            )
                        except Exception:
                            """
                            Se não conseguir fazer o depósito,
                            faz o estorno na conta de origem
                            """
                            deposito_conta_corrente(
                                account.id, account.numero, value)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                except Exception:
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                # Se não coseguir fazer o saque.
                QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                return
        # Mesma lógica da conta corrente, só que para conta poupança
        if account_source_type == "cp":
            if not valida_senha_conta_poupanca(account.id, password):
                QtWidgets.QMessageBox.warning(None, "Erro", "Senha incorreta!")
                return
            try:
                saque_conta_poupanca(
                    account.id,
                    account.numero,
                    value,
                    True,
                    target_user_id,
                    "cc" if target_account_type == "Conta Corrente" else "cp",
                )
                account.saca(value)
                try:
                    if target_account_type == "Conta Corrente":
                        try:
                            deposito_conta_corrente(
                                cc.id,
                                cc.numero,
                                value,
                                True,
                                user.id,
                                account_source_type,
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            new_cc = busca_conta_por_cpf(user.cpf, "cc")
                            user.add_cc(new_cc)
                            self.openContas(
                                MainWindow, user, account, account_source_type
                            )
                        except Exception:
                            deposito_conta_poupanca(
                                account.id, account.numero, value)
                            account.deposita(value)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                    else:
                        try:
                            deposito_conta_poupanca(
                                cp.id,
                                cp.numero,
                                value,
                                True,
                                user.id,
                                account_source_type,
                            )
                            QtWidgets.QMessageBox.information(
                                None, "Sucesso", "Transferência concluida!"
                            )
                            self.openContas(
                                MainWindow, user, account, account_source_type
                            )
                        except Exception:
                            deposito_conta_poupanca(
                                account.id, account.numero, value)
                            account.deposita(value)
                            QtWidgets.QMessageBox.warning(
                                None,
                                "Erro",
                                "Transação não concluida, valor estornado!",
                            )
                            return
                except Exception:
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "CPF não encontrado!")
                    return
            except Exception as E:
                QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                return

    def depositar(
        self, MainWindow, user, value, account, account_type, password
    ):
        try:
            # Verifica se o valor passado é um valor númerico
            value = float(value)
        except Exception:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return
        # Verifica se campo valor está vazio
        if value == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        else:
            # Verifica o tipo da conta e faz o depósito
            if account_type == "cc":
                # Verifica se a senha está correta
                if not valida_senha_conta_corrente(account.id, password):
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "Senha incorreta!")
                    return
                try:
                    # Faz o depósito
                    deposito_conta_corrente(account.id, account.numero, value)
                    account.deposita(value)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Depósito realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, account, account_type)
                except Exception as E:
                    # Se não conseguir fazer o depósito, mostra o erro
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return
            # Mesma lógica da conta corrente, só que para conta poupança
            if account_type == "cp":
                if not valida_senha_conta_poupanca(account.id, password):
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "Senha incorreta!")
                    return
                try:
                    deposito_conta_poupanca(account.id, account.numero, value)
                    account.deposita(value)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Depósito realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, account, account_type)
                except Exception as E:
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return

    def sacar(self, MainWindow, user, value, account, account_type, password):
        try:
            # Verifica se o valor passado é um valor numérico
            value = float(value)
        except Exception:
            QtWidgets.QMessageBox.warning(None, "Erro", "Valor inválido!")
            return
        # Verifica o campo está vazio
        if value == "":
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        else:
            # Verifica se o tipo da conta é conta corrente
            if account_type == "cc":
                # Verifica se a senha é válida
                if not valida_senha_conta_corrente(account.id, password):
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "Senha incorreta!")
                    return
                try:
                    # Realiza o saque
                    saque_conta_corrente(account.id, account.numero, value)
                    account.saca(value)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Saque realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, account, account_type)
                except Exception as E:
                    # Caso ocorra algum erro, exibe a mensagem de erro
                    QtWidgets.QMessageBox.warning(None, "Erro", str(E))
                    return
            # Mesma lógica da conta corrente, só que para conta poupança
            if account_type == "cp":
                if not valida_senha_conta_poupanca(account.id, password):
                    QtWidgets.QMessageBox.warning(
                        None, "Erro", "Senha incorreta!")
                    return
                try:
                    saque_conta_poupanca(account.id, account.numero, value)
                    account.saca(value)
                    QtWidgets.QMessageBox.information(
                        None, "Sucesso", "Saque realizado com sucesso!"
                    )
                    self.openContas(MainWindow, user, account, account_type)
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
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Preencha todos os campos!")
            return
        if len(infos[4]) < 8:
            QtWidgets.QMessageBox.warning(None, "Erro", "Senha muito curta!")
            return
        if len(infos[4]) > 45:
            QtWidgets.QMessageBox.warning(
                None, "Erro", "Senha muito comprida!"
            )
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
    def mostraSaldo(state, label, balance):
        if state.isChecked():
            label.setText(f"Saldo : R$ {balance:.2f}".replace(".", ","))
        else:
            label.setText(
                f"Saldo : R$ {'*' * len(str(balance))}".replace(".", ",")
            )

    @staticmethod
    def mostraSenha(check, password):
        if check.isChecked():
            password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            password.setEchoMode(QtWidgets.QLineEdit.Password)

    @staticmethod
    def convertDate(date):
        date = date.split("/")
        return f"{date[2]}-{date[1]}-{date[0]}"

    @staticmethod
    def atualizaContas(
        user, source_account_type, target_cpf_input, select_input
    ):
        cc = busca_conta_por_cpf(target_cpf_input.text(), "cc")
        cp = busca_conta_por_cpf(target_cpf_input.text(), "cp")
        select_input.clear()
        if user.cpf == target_cpf_input.text():
            if source_account_type == "cc":
                if cp:
                    select_input.addItem(f"Conta Poupança - {cp.numero}")
            elif source_account_type == "cp":
                if cc:
                    select_input.addItem(f"Conta Corrente - {cc.numero}")
        else:
            if cc:
                select_input.addItem(f"Conta Corrente - {cc.numero}")
            if cp:
                select_input.addItem(f"Conta Poupança - {cp.numero}")

    def getInfos(self, registration_inputs_window):
        name = registration_inputs_window.nome.text()
        cpf = registration_inputs_window.cpf.text()
        email = registration_inputs_window.email.text()
        password = registration_inputs_window.senha.text()
        birth = self.convertDate(registration_inputs_window.nascimento.text())
        return name, cpf, birth, email, password
