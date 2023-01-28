import mysql.connector as conex
from datetime import datetime
from client_obj import Cliente
from account_obj import ContaCorrente, ContaPoupanca


conection = conex.connect(
    host="localhost", user="myuser", password="mypassword", database="mydb"
)


def add_cliente(nome, cpf, nascimento, email, senha):
    cursor = conection.cursor()
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
    except Exception as E:
        duplicatad_camp = str(E).split("'")
        raise Exception(
            f"O {duplicatad_camp[-2]} {duplicatad_camp[1]} já está cadastrado!"
        )
    conection.commit()
    cursor.close()


def get_cliente_id_by_cpf(cpf):
    cursor = conection.cursor()
    result = cursor.execute(
        "SELECT idcliente FROM cliente WHERE cpf = (%s)", (cpf,))
    result = cursor.fetchone()[0]
    return result


def login(email, password):
    cursor = conection.cursor()
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


def create_conta_corrente(id, password):
    tot_accounts = conection.cursor()
    tot_accounts.execute(
        "SELECT max(idconta_corrente) FROM conta_corrente")
    tot_accounts = tot_accounts.fetchone()
    if tot_accounts[0] == None:
        tot_accounts = (0,)
    numero_da_conta = tot_accounts[0] + 100000

    cursor = conection.cursor()
    criation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conta_corrente (numero, senha, cliente_idcliente, saldo, criacao, limite) VALUES (%s,MD5(%s), %s, %s, %s, %s)",
        (
            numero_da_conta,
            password,
            id,
            0,
            criation_date,
            800,
        ),
    )
    conection.commit()
    cursor = conection.cursor()
    cursor.execute(
        f"SELECT idconta_corrente FROM conta_corrente WHERE numero = {numero_da_conta}"
    )
    id_conta = cursor.fetchone()[0]

    account = ContaCorrente(id_conta, numero_da_conta, password, criation_date, 0, 800)
    cursor.close()
    return account


def create_conta_poupanca(id, password):
    tot_accounts = conection.cursor()
    tot_accounts.execute(
        "SELECT max(idconta_poupanca) FROM conta_poupanca")
    tot_accounts = tot_accounts.fetchone()
    if tot_accounts[0] == None:
        tot_accounts = (0,)
    cursor = conection.cursor()
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conta_poupanca (numero, senha, cliente_idcliente, saldo, criacao) VALUES (%s, MD5(%s), %s, %s, %s)",
        (
            int(tot_accounts[0]) + 100000,
            password,
            id,
            0,
            creation_date,
        ),
    )
    conection.commit()
    cursor = conection.cursor()
    cursor.execute(
        f"SELECT idconta_poupanca FROM conta_poupanca WHERE numero = {int(tot_accounts[0])+100000}"
    )
    account_id = cursor.fetchone()[0]
    account = ContaPoupanca(
        account_id, int(tot_accounts[0]) + 100000, password, creation_date, 0
    )
    cursor.close()
    return account


def get_conta_corrente(id):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT * FROM conta_corrente WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    try:
        result = result[0]
    except:
        return None
    try:
        # 0 = id, 1 = numero, 2 = senha, 3 = saldo, 4 = limite, 5 = criacao
        account = ContaCorrente(
            result[0], result[1], result[2], result[5], result[3], result[4]
        )
    except:
        account = None
    cursor.close()
    return account


def get_conta_poupanca(id):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT * FROM conta_poupanca WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    try:
        result = result[0]
    except:
        return None
    try:
        account = ContaPoupanca(result[0], result[1],
                              result[2], result[4], result[3])
    except:
        account = None
    cursor.close()
    return account


def valida_senha_conta_corrente(id, password):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT * FROM conta_corrente WHERE idconta_corrente = %s AND senha = MD5(%s)",
        (id, password),
    )
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


def valida_senha_conta_poupanca(id, password):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT * FROM conta_poupanca WHERE idconta_poupanca = %s AND senha = MD5(%s)",
        (id, password),
    )
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


def add_transacao(account_id, account_type, value, description):
    cursor = conection.cursor()
    if account_type == "cc":
        cursor.execute(
            f"INSERT INTO historico (momento, tipo, valor, conta_corrente_idconta_corrente) VALUES ('{str(datetime.now()).split('.')[0]}', '{description}', '{value}', '{account_id}')"
        )
    else:
        cursor.execute(
            f"INSERT INTO historico (momento, tipo, valor, conta_poupanca_idconta_poupanca) VALUES ('{str(datetime.now()).split('.')[0]}', '{description}', '{value}', '{account_id}')"
        )

    conection.commit()
    cursor.close()


def get_transacoes(account_id, account_type):
    if isinstance(account_id, tuple):
        account_id = account_id[0]
    cursor = conection.cursor()
    if account_type == "cc":
        cursor.execute(
            f"SELECT * FROM historico WHERE conta_corrente_idconta_corrente = {account_id}"
        )
    else:
        cursor.execute(
            f"SELECT * FROM historico WHERE conta_poupanca_idconta_poupanca = {account_id}"
        )
    result = cursor.fetchall()
    cursor.close()
    return result


def deposito_conta_corrente(
    account_id, account_number, value, transfer=False, source_user_id=None, source_account_type=None
):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT saldo FROM conta_corrente WHERE numero = %s", (account_number,))
    result = cursor.fetchone()
    if value <= 0:
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
        (result[0] + value, account_number),
    )
    if transfer:
        if source_account_type == "cc":
            source_account = get_conta_corrente(source_user_id)
        elif source_account_type == "cp":
            source_account = get_conta_poupanca(source_user_id)
        else:
            source_account = None
        source_user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (source_user_id,)
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
    conection.commit()
    cursor.close()
    return True, "Depósito realizado com sucesso!"


def deposito_conta_poupanca(
    account_id, account_number, value, transfer=False, source_user_id=None, source_account_type=None
):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT saldo FROM conta_poupanca WHERE numero = %s", (account_number,))
    result = cursor.fetchone()
    if value <= 0:
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
        (result[0] + value, account_number),
    )
    if transfer:
        if source_account_type == "cc":
            source_account = get_conta_corrente(source_user_id)
        elif source_account_type == "cp":
            source_account = get_conta_poupanca(source_user_id)
        else:
            source_account = None

        source_user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (source_user_id,)
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
    conection.commit()
    cursor.close()
    return True, "Depósito realizado com sucesso!"


def saque_conta_corrente(
    account_id, account_number, value, transfer=False, target_user_id=None, target_account_type=None
):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT saldo, limite FROM conta_corrente WHERE numero = %s", (account_number,)
    )
    result = cursor.fetchone()
    if result[1] < value:
        cursor.close()
        raise Exception("Limite atingido!")
    if result[0] < value:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if value <= 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
        (result[0] - value, account_number),
    )
    if transfer:
        if target_account_type == "cc":
            target_account = get_conta_corrente(target_user_id)
        elif target_account_type == "cp":
            target_account = get_conta_poupanca(target_user_id)
        else:
            target_account = None
        target_user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (target_user_id,)
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
    conection.commit()
    cursor.close()
    return True, "Saque realizado com sucesso!"


def saque_conta_poupanca(
    account_id, account_number, value, transfer=False, target_user_id=None, target_account_type=None
):
    cursor = conection.cursor()
    cursor.execute(
        "SELECT saldo FROM conta_poupanca WHERE numero = %s", (account_number,))
    result = cursor.fetchone()
    if result[0] < value:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if value <= 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
        (result[0] - value, account_number),
    )
    if transfer:
        if target_account_type == "cc":
            target_account = get_conta_corrente(target_user_id)
        elif target_account_type == "cp":
            target_account = get_conta_poupanca(target_user_id)
        else:
            target_account = None
        target_user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (target_user_id,)
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
    conection.commit()
    cursor.close()
    return True, "Saque realizado com sucesso!"


def busca_conta_por_cpf(cpf, account_type):
    cursor = conection.cursor()
    cursor.execute("SELECT * FROM cliente WHERE cpf = %s", (cpf,))
    try:
        user_id = cursor.fetchone()[0]
        cursor.close()
    except:
        return None
    if account_type == "cc":
        return get_conta_corrente(user_id)
    else:
        return get_conta_poupanca(user_id)
