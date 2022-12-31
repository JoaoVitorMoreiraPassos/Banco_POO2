class Cliente():

    __slots__ = ['_id',"_nome", "_cpf", "_nascimento", "_email", "_contas"]
    
    def __init__(self, id, nome, cpf, nascimento, email):
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._nascimento = nascimento
        self._email = email
        self._contas = {}

    def add_cc(self, conta):
        self._contas["cc"] = conta
    
    def add_cp(self, conta):
        self._contas["cp"] = conta
        
    def __str__(self):
        return f"id: {self._id} | Nome: {self._nome} | CPF: {self._cpf} | Nascimento: {self._nascimento} | Email: {self._email}"
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nome):
        self._nome = nome
        
    @property
    def cpf(self):
        return self._cpf
    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def nascimento(self):
        return self._nascimento
    @nascimento.setter
    def nascimento(self, nascimento):
        self._nascimento = nascimento
        
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email
        
    @property
    def contas(self):
        return self._contas
    