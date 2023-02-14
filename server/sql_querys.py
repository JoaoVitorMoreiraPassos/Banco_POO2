import mysql.connector as conex
from datetime import datetime
from client_obj import Cliente
from account_obj import ContaCorrente, ContaPoupanca
    """
    test
    """

def connect():
    """
    Função para fazer a conexão com banco de dados

            Parameters:
                    None
            Returns:
                    conexão com o banco de dados
    """
    return conex.connect(
        host="localhost", user="myuser", password="mypassword", database="mydb"
    )


def add_cliente(nome, cpf, nascimento, email, senha):
    """
    Função para adicionar um cliente no banco de dados.

            Parameters:
                    nome (str): nome do cliente.
                    cpf (str): cpf do cliente.
                    nascimento (str): data de nascimento do cliente.
                    email (str): email do cliente.
                    senha (str): senha do cliente.

            Returns:
                    conexão com o banco de dados.
    """
    with connect() as conection:
        with conection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO cliente (nome, cpf, nascimento, email, senha_acesso, criacao) VALUES (%s, %s, %s, %s, MD5(%s), %s)",
                    (
                        nome,
                        cpf,
                        nascimento,
                        email,
                        senha,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )
                conection.commit()
            except Exception as E:
                cursor.close()
                conection.close()
                duplicatad_camp = str(E).split("'")
                raise Exception(
                    f"O {duplicatad_camp[-2]} {duplicatad_camp[1]} já está cadastrado!"
                )


def get_cliente_id_by_cpf(cpf):
    """
    Busca o id de cliente no banco de dados pelo cpf.

            Parameters:
                    cpf (str): cpf do cliente.
            Returns:
                    result (int): id do cliente.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            result = cursor.execute(
                "SELECT idcliente FROM cliente WHERE cpf = (%s)", (cpf,))
            result = cursor.fetchone()[0]
    return result


def login(email, password):
    """
    Função para fazer o login do cliente. 

            Parameters:
                    email (str): email do cliente.
                    password (str): senha do cliente.
            Returns:
                    result (tuple): (True, client) se o login foi bem sucedido,
                    (False, None) se não.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM cliente WHERE email = %s AND senha_acesso = MD5(%s)",
                (email, password),
            )
            result = cursor.fetchone()
    if result:
        # 0 = id, 4 = nome, 1 = cpf, 2 = nascimento, 3 = email
        client = Cliente(result[0], result[4],
                         result[1], result[2], result[3])
        cc = get_conta_corrente(client.id)
        cp = get_conta_poupanca(client.id)
        if cc:
            client.add_cc(cc)
        if cp:
            client.add_cp(cp)
        return True, client
    else:
        return False, None


def get_user_by_id(id):
    """
    Busca o cliente no banco de dados pelo id.

            Parameters:
                    id (int): id do cliente.
            Returns:
                    result (Cliente): objeto do tipo cliente se a conta for
                    encontrada e None se não for.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM cliente WHERE idcliente = %s", (id,))
            result = cursor.fetchone()
    if result:
        # 0 = id, 4 = nome, 1 = cpf, 2 = nascimento, 3 = email
        client = Cliente(result[0], result[4],
                         result[1], result[2], result[3])
        cc = get_conta_corrente(client.id)
        cp = get_conta_poupanca(client.id)
        if cc:
            client.add_cc(cc)
        if cp:
            client.add_cp(cp)
        return client
    else:
        return None


def create_conta_corrente(user_id, account_password):
    """
    Função para adiconar uma conta corrente no banco de dados.

            Parameters:
                    user_id (int): id do cliente.
                    account_password (str): senha da conta.
            Returns:
                    ContaCorrente: objeto do tipo conta corrente.
    """
    tot_accounts = None
    account_number = None
    criation_date = None
    account_id = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT max(idconta_corrente) FROM conta_corrente")
            tot_accounts = cursor.fetchone()
            if tot_accounts[0] == None:
                tot_accounts = (0,)
            account_number = tot_accounts[0] + 100000

            criation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO conta_corrente (numero, senha, cliente_idcliente, saldo, criacao, limite) VALUES (%s,MD5(%s), %s, %s, %s, %s)",
                (
                    account_number,
                    account_password,
                    user_id,
                    0,
                    criation_date,
                    800,
                ),
            )
            conection.commit()
            cursor.execute(
                f"SELECT idconta_corrente FROM conta_corrente WHERE numero = {account_number}"
            )
            account_id = cursor.fetchone()[0]
    return ContaCorrente(account_id, account_number, account_password, criation_date, 0, 800)


def create_conta_poupanca(user_id, account_password):
    """
    Função para adiconar uma conta poupança no banco de dados.

            Parameters:
                    user_id (int): id do cliente.
                    account_password (str): senha da conta.
            Returns:
                    ContaPoupanca: objeto do tipo conta poupança.
    """
    tot_accounts = None
    account_number = None
    creation_date = None
    account_id = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT max(idconta_poupanca) FROM conta_poupanca")
            tot_accounts = cursor.fetchone()
            if tot_accounts[0] == None:
                tot_accounts = (0,)
            account_number = tot_accounts[0] + 100000
            creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO conta_poupanca (numero, senha, cliente_idcliente, saldo, criacao) VALUES (%s, MD5(%s), %s, %s, %s)",
                (
                    account_number,
                    account_password,
                    user_id,
                    0,
                    creation_date,
                ),
            )
            conection.commit()
            cursor.execute(
                f"SELECT idconta_poupanca FROM conta_poupanca WHERE numero = {account_number}"
            )
            account_id = cursor.fetchone()[0]
    return ContaPoupanca(
        account_id, account_number, account_password, creation_date, 0
    )


def get_conta_corrente(id):
    """
    Função para buscar uma conta corrente no banco de dados.

            Parameters:
                    id (int): id do cliente.
            Returns:
                    ContaCorrente: objeto do tipo conta corrente se a busca for 
                    bem sucessida, senão retorna None.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM conta_corrente WHERE cliente_idcliente = %s", (id,))
            result = cursor.fetchall()
    try:
        result = result[0]
    except Exception:
        return None
    try:
        # 0 = id, 1 = numero, 2 = senha, 3 = saldo, 4 = limite, 5 = criacao
        return ContaCorrente(
            result[0], result[1], result[2], result[5], result[3], result[4]
        )
    except Exception:
        return None


def get_conta_poupanca(id):
    """
    Função para buscar uma conta poupança no banco de dados.

            Parameters:
                    id (int): id do cliente.
            Returns:
                    ContaPoupanca: objeto do tipo conta poupança se a busca for
                    bem sucessida, senão retorna None.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor = conection.cursor()
            cursor.execute(
                "SELECT * FROM conta_poupanca WHERE cliente_idcliente = %s", (id,))
            result = cursor.fetchall()
    try:
        result = result[0]
    except:
        return None
    try:
        return ContaPoupanca(result[0], result[1],
                             result[2], result[4], result[3])
    except:
        return None


def valida_senha_conta_corrente(id, password):
    """
    Função para validar a senha de uma conta corrente.

            Parameters:
                    id (int): id da conta corrente.
                    password (str): senha da conta corrente.
            Returns:
                    bool: True se a senha for válida, senão retorna False.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM conta_corrente WHERE idconta_corrente = %s AND senha = MD5(%s)",
                (id, password),
            )
            result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def valida_senha_conta_poupanca(id, password):
    """
    Função para validar a senha de uma conta poupança.

            Parameters:
                    id (int): id da conta poupança.
                    password (str): senha da conta poupança.
            Returns:
                    bool: True se a senha for válida, senão retorna False.
    """
    result = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM conta_poupanca WHERE idconta_poupanca = %s AND senha = MD5(%s)",
                (id, password),
            )
            result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def add_transacao(account_id, account_type, value, description):
    """
    Função para adicionar uma transação no banco de dados.

            Parameters: 
                    account_id (int): id da conta.
                    account_type (str): tipo da conta.
                    value (float): valor da transação.
                    description (str): descrição da transação.
            Returns:
                    None.
    """
    with connect() as conection:
        with conection.cursor() as cursor:
            if account_type == "cc":
                cursor.execute(
                    f"INSERT INTO historico (momento, tipo, valor, conta_corrente_idconta_corrente) VALUES ('{str(datetime.now()).split('.')[0]}', '{description}', '{value}', '{account_id}')"
                )
            else:
                cursor.execute(
                    f"INSERT INTO historico (momento, tipo, valor, conta_poupanca_idconta_poupanca) VALUES ('{str(datetime.now()).split('.')[0]}', '{description}', '{value}', '{account_id}')"
                )
        conection.commit()


def get_transacoes(account_id, account_type):
    """
    Função para buscar as transações de uma conta.

            Parameters:
                    account_id (int): id da conta.
                    account_type (str): tipo da conta.
            Returns:
                    result (tuple): tupla de transações.
    """
    result = None
    if isinstance(account_id, tuple):
        account_id = account_id[0]
    with connect() as conection:
        with conection.cursor() as cursor:
            if account_type == "cc":
                cursor.execute(
                    f"SELECT * FROM historico WHERE conta_corrente_idconta_corrente = {account_id}"
                )
            else:
                cursor.execute(
                    f"SELECT * FROM historico WHERE conta_poupanca_idconta_poupanca = {account_id}"
                )
            result = cursor.fetchall()
    return result


def deposito_conta_corrente(
    account_id, account_number, value, transfer=False, source_user_id=None, source_account_type=None
):
    """
    Função para aumentar o saldo de uma conta corrente.

            Parameters:
                    account_id (int): id da conta corrente.
                    account_number (str): número da conta corrente.
                    value (float): valor a ser depositado.
                    transfer (bool): se a transação é uma transferência.
                    source_user_id (int): id do usuário que está transferindo.
                    source_account_type (str): tipo da conta que está transferindo.
            Returns:
                    Tuple: (True, mensagem) se a função executar sem erros.
    """
    source_account = None
    source_user = None
    if value <= 0:
        raise Exception("Valor inválido!")
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo FROM conta_corrente WHERE numero = %s", (account_number,))
            result = cursor.fetchone()
            cursor.execute(
                "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
                (result[0] + value, account_number),
            )
            conection.commit()
    if transfer:
        if source_account_type == "cc":
            source_account = get_conta_corrente(source_user_id)
        elif source_account_type == "cp":
            source_account = get_conta_poupanca(source_user_id)
        else:
            source_account = None
        with connect() as conection:
            with conection.cursor() as cursor:
                source_user = cursor.execute(
                    "SELECT nome FROM cliente WHERE idcliente = %s", (
                        source_user_id,)
                )
                source_user = cursor.fetchone()[0]
        add_transacao(
            account_id,
            "cc",
            value,
            f"transferência recebida da conta {'corrente' if source_account_type == 'cc' else 'poupanca'} nº {source_account.numero} de {source_user}",
        )
    else:
        add_transacao(account_id, "cc", value, "deposito")
    return True, "Depósito realizado com sucesso!"


def deposito_conta_poupanca(
    account_id, account_number, value, transfer=False, source_user_id=None, source_account_type=None
):
    """
    Função para aumentar o saldo de uma conta poupanca.

            Parameters:
                    account_id (int): id da conta poupanca.
                    account_number (str): número da conta poupanca.
                    value (float): valor a ser depositado.
                    transfer (bool): se a transação é uma transferência.
                    source_user_id (int): id do usuário que está transferindo.
                    source_account_type (str): tipo da conta que está transferindo.
            Returns:
                    Tuple: (True, mensagem) se a função executar sem erros.
    """
    source_account = None
    source_user = None
    if value <= 0:
        raise Exception("Valor inválido!")
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo FROM conta_poupanca WHERE numero = %s", (account_number,))
            result = cursor.fetchone()
            cursor.execute(
                "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
                (result[0] + value, account_number),
            )
            conection.commit()
    if transfer:
        if source_account_type == "cc":
            source_account = get_conta_corrente(source_user_id)
        elif source_account_type == "cp":
            source_account = get_conta_poupanca(source_user_id)
        else:
            source_account = None
        with connect() as conection:
            with conection.cursor() as cursor:
                source_user = cursor.execute(
                    "SELECT nome FROM cliente WHERE idcliente = %s", (
                        source_user_id,)
                )
                source_user = cursor.fetchone()[0]
        add_transacao(
            account_id,
            "cp",
            value,
            f"transferência recebida da conta {'corrente' if source_account_type == 'cc' else 'poupanca'} nº {source_account.numero} de {source_user}",
        )
    else:
        add_transacao(account_id, "cp", value, "deposito")
    return True, "Depósito realizado com sucesso!"


def saque_conta_corrente(
    account_id, account_number, value, transfer=False, target_user_id=None, target_account_type=None
):
    """
    Função para diminuir o saldo de uma conta corrente.

            Parameters:
                    account_id (int): id da conta corrente.
                    account_number (str): número da conta corrente.
                    value (float): valor a ser depositado.
                    transfer (bool): se a transação é uma transferência.
                    source_user_id (int): id do usuário que está transferindo.
                    source_account_type (str): tipo da conta que está transferindo.
            Returns:
                    Tuple: (True, mensagem) se a função executar sem erros.
    """
    target_account = None
    target_user = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo, limite FROM conta_corrente WHERE numero = %s", (
                    account_number,)
            )
            result = cursor.fetchone()
    if result[1] < value:
        raise Exception("Limite atingido!")
    if result[0] < value:
        raise Exception("Saldo insuficiente!")
    if value <= 0:
        raise Exception("Valor inválido!")
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
                (result[0] - value, account_number),
            )
            conection.commit()
    if transfer:
        if target_account_type == "cc":
            target_account = get_conta_corrente(target_user_id)
        elif target_account_type == "cp":
            target_account = get_conta_poupanca(target_user_id)
        else:
            target_account = None
        with connect() as conection:
            with conection.cursor() as cursor:
                target_user = cursor.execute(
                    "SELECT nome FROM cliente WHERE idcliente = %s", (
                        target_user_id,)
                )
                target_user = cursor.fetchone()[0]
        add_transacao(
            account_id,
            "cc",
            value,
            f"transferência realizada para conta {'corrente' if target_account_type == 'cc' else 'poupanca'} nº {target_account.numero} de {target_user}",
        )
    else:
        add_transacao(account_id, "cc", value, "saque")
    return True, "Saque realizado com sucesso!"


def saque_conta_poupanca(
    account_id, account_number, value, transfer=False, target_user_id=None, target_account_type=None
):
    """
    Função para diminuir o saldo de uma conta poupanca.

            Parameters:
                    account_id (int): id da conta poupanca.
                    account_number (str): número da conta poupanca.
                    value (float): valor a ser depositado.
                    transfer (bool): se a transação é uma transferência.
                    source_user_id (int): id do usuário que está transferindo.
                    source_account_type (str): tipo da conta que está transferindo.
            Returns:
                    Tuple: (True, mensagem) se a função executar sem erros.
    """
    target_account = None
    target_user = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo FROM conta_poupanca WHERE numero = %s", (account_number,))
            result = cursor.fetchone()
            if result[0] < value:
                cursor.close()
                conection.close()
                raise Exception("Saldo insuficiente!")
            if value <= 0:
                cursor.close()
                conection.close()
                raise Exception("Valor inválido!")
            cursor.execute(
                "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
                (result[0] - value, account_number),
            )
            conection.commit()
    if transfer:
        if target_account_type == "cc":
            target_account = get_conta_corrente(target_user_id)
        elif target_account_type == "cp":
            target_account = get_conta_poupanca(target_user_id)
        else:
            target_account = None
        with connect() as conection:
            with conection.cursor() as cursor:
                target_user = cursor.execute(
                    "SELECT nome FROM cliente WHERE idcliente = %s", (
                        target_user_id,)
                )
                target_user = cursor.fetchone()[0]
        add_transacao(
            account_id,
            "cp",
            value,
            f"transferência realizada para conta {'corrente' if target_account_type == 'cc' else 'poupanca'} nº {target_account.numero} de {target_user}",
        )
    else:
        add_transacao(account_id, "cp", value, "saque")
    return True, "Saque realizado com sucesso!"


def busca_conta_por_cpf(cpf, account_type):
    """
    Função para buscar uma conta corrente ou poupança pelo cpf do usuário.

            Parameters:
                    cpf (str): cpf do usuário.
                    account_type (str): tipo da conta a ser buscada.
            Returns:
                    ContaCorrente ou ContaPoupanca: conta encontrada.
    """
    user_id = None
    with connect() as conection:
        with conection.cursor() as cursor:
            cursor.execute("SELECT * FROM cliente WHERE cpf = %s", (cpf,))
            try:
                user_id = cursor.fetchone()[0]
            except:
                return None
    if account_type == "cc":
        return get_conta_corrente(user_id)
    else:
        return get_conta_poupanca(user_id)
