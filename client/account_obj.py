from datetime import datetime

# from sgbd import get_conta_corrente, get_conta_poupanca


class Historico:
    """
    A classe representa o histórico de transações de uma conta.

    ...

    Attributes
    ----------
    data_abertura : datetime
        data de abertura da conta
    transacoes : list
        lista de transações

    Methods
    -------
    imprime():
        Mostra o histórico de transações de uma conta

    """

    __slots__ = ["data_abertura", "transacoes"]

    def __init__(self):
        self.data_abertura = datetime.today()
        self.transacoes = []

    def imprime(self):
        print("-" * 60)
        print("data de abertura: {}".format(self.data_abertura))
        print("transações: ")
        for transacao in self.transacoes:
            print("-", transacao)


class Conta:
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
        self.historico.imprime()
        print(
            "- {} - Saldo de {} do cliente {}".format(
                datetime.today(), self.saldo, self.cliente.nome
            )
        )
        print("-" * 60)


class ContaCorrente(Conta):
    __slots__ = ["_numero", "_senha", "_criacao", "_saldo", "_limite", "_historico"]

    def __init__(self, id, numero, senha, criacao, saldo=0, limite=800):
        super().__init__(id, numero, senha, criacao, saldo)
        self._limite = limite

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, limite):
        self._limite = limite

    def transfere(self, conta_destino, valor):
        if self.saldo < valor:
            return False, "Saldo insuficiente"
        if valor < 0:
            return False, "Valor inválido"

        self.saldo -= valor
        conta_destino.saldo += valor


class ContaPoupanca(Conta):
    __slots__ = ["_numero", "_senha", "_criacao", "_saldo", "_limite", "_historico"]

    def __init__(self, id, numero, senha, criacao, saldo=0):
        super().__init__(id, numero, senha, criacao, saldo)

    def deposita(self, valor):
        return super().deposita(valor)

    def saca(self, valor):
        return super().saca(valor)

    def transfere(self, conta_destino, valor):
        if self.saldo < valor:
            return False, "Saldo insuficiente"
        if valor < 0:
            return False, "Valor inválido"

        self.saldo -= valor
        conta_destino.saldo += valor
