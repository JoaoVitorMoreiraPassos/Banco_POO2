from datetime import datetime

# from sgbd import get_conta_corrente, get_conta_poupanca


class Historico:

    """
    __slots__ = ["data_abertura", "transacoes"]

    def __init__(self):
        """
        Método construtor da classe Historico

        Parameters
        ----------
        None: None

        Returns
        -------
        None
        """
        self.data_abertura = datetime.today()
        self.transacoes = []

    def imprime(self):
        """
        Mosta o histórico de transações de uma conta que estão armazenadas na lista de transações.

        Parameters
        ----------
        None: None

        Returns
        -------
        None
        """
        print("-" * 60)
        print("data de abertura: {}".format(self.data_abertura))
        print("transações: ")
        for transacao in self.transacoes:
            print("-", transacao)


class Conta:
    """
    A classe representa uma conta de um banco.

    ...

    Attributes
    ----------
    id : int
        id da conta bancária
    numero : int
        número da conta bancária
    senha : int
        senha da conta bancária
    saldo : float
        saldo da conta bancária
    criacao : datetime
        data de criação da conta bancária
    historico : Historico
        histórico de transações da conta bancária
    total_contas : int
        total de contas bancárias

    Methods
    -------
    get_total_contas():
        Retorna o total de contas bancárias.
    deposita(valor, transferencia=False):
        Realiza um depósito na conta bancária.
    saca(valor, transferencia=False):
        Realiza um saque na conta bancária.
    extrato():
        Mostra o extrato da conta bancária.
    """

    __slots__ = [
        "_id",
        "_numero",
        "_senha",
        "_criacao",
        "_saldo",
        "_limite",
        "_historico",
    ]
    _total_contas = 0

    def __init__(self, id, numero, senha, criacao, saldo=0):
        """
        Método construtor da classe Conta.
        
        Parameters
        ----------
        id : int
            id da conta bancária
        numero : int
            número da conta bancária
        senha : int
            senha da conta bancária
        saldo : float, opcional
            saldo da conta bancária(default é 0)
        criacao : datetime
            data de criação da conta bancária
        historico : Historico
            histórico de transações da conta bancária
        total_contas : int
            total de contas bancárias
        
        Returns
        -------
        None
        """
        self._id = id
        self._numero = numero
        self._senha = senha
        self._saldo = saldo
        self._criacao = criacao
        self._historico = Historico()
        Conta._total_contas += 1

    @staticmethod
    def get_total_contas():
        return Conta._total_contas

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, senha):
        self._senha = senha

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo):
        self._saldo = saldo

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, limite):
        self._limite = limite

    @property
    def historico(self):
        return self._historico

    @property
    def criacao(self):
        return self._criacao

    def deposita(self, valor, transferencia=False):
        """
        Método que realiza um depósito na conta bancária.

        Parameters
        ----------
        valor : float
            valor a ser depositado na conta bancária
        transferencia : bool, opcional
            indica se o depósito é uma transferência (default é False)
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem
        """
        try:
            valor = float(valor)
        except Exception:
            return False, "Valor inválido"
        if valor < 0:
            return False, "Valor inválido"

        self.saldo += valor
        if transferencia:
            self.historico.transacoes.append(
                "{} - Transferência recebida - valor: {}".format(
                    datetime.today(), valor
                )
            )
            return True, "Transferência realizada com sucesso"
        else:
            self.historico.transacoes.append(
                "{} - Depósito - valor: {}".format(datetime.today(), valor)
            )
            return True, "Depósito realizado com sucesso"

    def saca(self, valor, transferencia=False):
        """
        Método que realiza um saque na conta bancária.

        Parameters
        ----------
        valor : float
            valor a ser sacado na conta bancária
        transferencia : bool, opcional
            indica se o saque é uma transferência (default é False)
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem
        """
        try:
            valor = float(valor)
        except Exception:
            return False, "Valor inválido"
        if valor > self.saldo:
            return False, "Saldo insuficiente"
        if valor < 0:
            print("foi aqui")
            return False, "Valor inválido"

        self.saldo -= valor
        if transferencia:
            self.historico.transacoes.append(
                "{} - Transferência realizada - valor: {}".format(
                    datetime.today(), valor
                )
            )
            return True, "Transferência realizada com sucesso"
        else:
            self.historico.transacoes.append(
                "{} - Saque - valor: {}".format(datetime.today(), valor)
            )
            return True, "Saque realizado com sucesso"

    def extrato(self):
        """
        Método que imprime o extrato da conta bancária.

        Parameters
        ----------
        None: None

        Returns
        -------
        None
        """
        self.historico.imprime()
        print(
            "- {} - Saldo de {} do cliente {}".format(
                datetime.today(), self.saldo, self.cliente.nome
            )
        )
        print("-" * 60)


class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente e herda da classe Conta.

    Attributes
    ----------
    id : int
        id da conta bancária
    numero : int
        número da conta bancária
    senha : int
        senha da conta bancária
    criacao : datetime
        data de criação da conta bancária
    saldo : float
        saldo da conta bancária
    limite : float
        limite da conta bancária
    historico : Historico
        histórico de transações da conta bancária

    Methods
    -------
    transfere(conta_destino, valor):
        Realiza uma transferência entre contas.
    """
    __slots__ = ["_numero", "_senha", "_criacao", "_saldo", "_limite", "_historico"]

    def __init__(self, id, numero, senha, criacao, saldo=0, limite=800):
        """
        Construtor da classe ContaCorrente, que chama o construtor da classe Conta.

        Parameters
        ----------
        id : int
            id da conta bancária
        numero : int
            número da conta bancária
        senha : int
            senha da conta bancária
        criacao : datetime
            data de criação da conta bancária
        saldo : float, opcional
            saldo da conta bancária (default é 0)
        limite : float, opcional
            limite da conta bancária (default é 800)

        Returns
        -------
        None
        """
        super().__init__(id, numero, senha, criacao, saldo)
        self._limite = limite

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, limite):
        self._limite = limite

    def transfere(self, conta_destino, valor):
        """
        Método que realiza uma transferência entre contas.

        Parameters
        ----------
        conta_destino : Conta
            conta de destino da transferência
        valor : float
            valor a ser transferido
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem
        """
        if self.saldo < valor:
            return False, "Saldo insuficiente"
        if valor < 0:
            return False, "Valor inválido"

        self.saldo -= valor
        conta_destino.saldo += valor


class ContaPoupanca(Conta):
    """
    Classe que representa uma conta poupança e herda da classe Conta.

    Attributes
    ----------
    id : int
        id da conta bancária
    numero : int
        número da conta bancária
    senha : int
        senha da conta bancária
    criacao : datetime
        data de criação da conta bancária
    saldo : float
        saldo da conta bancária
    
    Methods
    -------
    deposita(valor):
        Realiza um depósito na conta bancária, chamando o método deposita da classe Conta.
    saca(valor):
        Realiza um saque na conta bancária, chamando o método saca da classe Conta.
    transfere(conta_destino, valor):
        Realiza uma transferência entre contas.
    """
    __slots__ = ["_numero", "_senha", "_criacao", "_saldo", "_limite", "_historico"]

    def __init__(self, id, numero, senha, criacao, saldo=0):
        """
        Construtor da classe ContaPoupanca, que chama o construtor da classe Conta.
        
        Parameters
        ----------
        id : int
            id da conta bancária
        numero : int
            número da conta bancária
        senha : int
            senha da conta bancária
        criacao : datetime
            data de criação da conta bancária
        saldo : float, opcional
            saldo da conta bancária (default é 0)
        
        Returns
        -------
        None
        """
        super().__init__(id, numero, senha, criacao, saldo)

    def deposita(self, valor):
        """
        Método que realiza um depósito na conta bancária, chamando o método deposita da classe Conta.

        Parameters
        ----------
        valor : float
            valor a ser depositado na conta bancária
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem que é retornada pelo método deposita da classe Conta
        """
        return super().deposita(valor)

    def saca(self, valor):
        """
        Método que realiza um saque na conta bancária, chamando o método saca da classe Conta.

        Parameters
        ----------
        valor : float
            valor a ser sacado da conta bancária
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem que é retornada pelo método saca da classe Conta
        """
        return super().saca(valor)

    def transfere(self, conta_destino, valor):
        """
        Método que realiza uma transferência entre contas.

        Parameters
        ----------
        conta_destino : Conta
            conta de destino da transferência
        valor : float
            valor a ser transferido
        
        Returns
        -------
        (bool, str): tupla com o status da operação e uma mensagem
        """
        if self.saldo < valor:
            return False, "Saldo insuficiente"
        if valor < 0:
            return False, "Valor inválido"

        self.saldo -= valor
        conta_destino.saldo += valor
