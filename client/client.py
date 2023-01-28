import socket
import datetime
from cliente_obj import Cliente
from account_obj import ContaCorrente, ContaPoupanca

"""
    Operações: 
    01 - Login,
    02 - Cadastro,
    03 - Busca por transações de uma conta,
    04 - Busca contas de um cliente por cpf,
    05 - saque em uma conta corrente,
    06 - saque em uma conta poupança,
    07 - criar uma conta corrente,
    08 - criar uma conta poupança,
    09 - buscar o id de um cliente pelo cpf,
    10 - depósito em um conta corrente,
    11 - depósito em uma conta poupança,
    12 - valida a senha de uma conta corrente,
    13 - valida a senha de uma conta poupança
"""

"""
    Funcionamento das funções:
        As funções recebem os dados necessários para a operação desejada, empacotam os dados em um json e enviam para o servidor que é responsável pela conexão e operações com o banco de dados mysql.
        O servidor retorna um json com o resultado da operação e informações necessárias para a funciolidade que o usuário deseja acessar no sistema.
"""


def connect():
    host = "0.0.0.0"
    port = 50001

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    return client


def login(email, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "01", "email": email, "senha": senha}
    data = str(data)
    client.send(data.encode())
    login_result = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se o login foi bem sucedido
    if login_result == "False":
        return False, None
    else:
        # Transforma o resultado em um objeto Cliente
        user = eval(login_result)
        temp = Cliente(
            user["id"], user["nome"], user["cpf"], user["nascimento"], user["email"]
        )
        # Transforma os dicionários em objetos ContaCorrente e ContaPoupança
        try:
            cc = user["contas"]["cc"]
            cc = ContaCorrente(
                cc["id"],
                cc["numero"],
                cc["senha"],
                cc["criacao"],
                cc["saldo"],
                cc["limite"],
            )
            temp.add_cc(cc)
        except Exception as E:
            pass
        try:
            cp = user["contas"]["cp"]
            cp = ContaPoupanca(
                cp["id"], cp["numero"], cp["senha"], cp["criacao"], cp["saldo"]
            )
            temp.add_cp(cp)
        except Exception as E:
            pass
        user = temp
        return True, user


def add_cliente(name, cpf, birth, email, password):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "02",
        "nome": name,
        "cpf": cpf,
        "nascimento": birth,
        "email": email,
        "senha": password,
    }
    data = str(data)
    client.send(data.encode())
    add_result = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se o cadastro foi bem sucedido e retorna o resultado para o usuário
    if add_result == "False":
        raise Exception("Erro ao adicionar cliente")
    else:
        return True, None


def get_transacoes(id, account_type):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "03", "id": id, "tipo": account_type}
    data = str(data)
    client.send(data.encode())
    trasactions_getter_result = client.recv(2048).decode()
    # Fecha a conexão
    client.close()
    # Verifica se a busca por transações foi bem sucessida e retorna o resultado para o usuário
    if trasactions_getter_result == "False":
        raise Exception("Erro ao adicionar cliente")
    else:
        return eval(trasactions_getter_result)


def busca_conta_por_cpf(cpf, account_type):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "04", "cpf": cpf, "tipo": account_type}
    data = str(data)
    client.send(data.encode())
    account_getter_result = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se a busca por transações foi bem sucessida e retorna o resultado para o usuário
    if account_getter_result == "False":
        return None
    else:
        account = eval(account_getter_result)
        if account_type == "cc":
            account = ContaCorrente(
                account["id"],
                account["numero"],
                account["senha"],
                account["criacao"],
                account["saldo"],
                account["limite"],
            )
        elif account_type == "cp":
            account = ContaPoupanca(
                account["id"],
                account["numero"],
                account["senha"],
                account["criacao"],
                account["saldo"],
            )
        return account


def saque_conta_corrente(
    id,
    account_number,
    value,
    transfer=False,
    target_user_id=None,
    target_account_target=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "05",
        "id": id,
        "numero": account_number,
        "valor": value,
        "transferencia": transfer,
        "id_user_destino": target_user_id,
        "tipo_conta_destino": target_account_target,
    }
    data = str(data)
    client.send(data.encode())

    withdraw_result = client.recv(1024).decode()
    # fecha a conexão
    client.close()
    if withdraw_result != "Saque realizado com sucesso!":
        raise Exception(withdraw_result)
    else:
        return True, withdraw_result


def saque_conta_poupanca(
    id,
    account_number,
    value,
    transfer=False,
    target_user_id=None,
    target_account_type=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "06",
        "id": id,
        "numero": account_number,
        "valor": value,
        "transferencia": transfer,
        "id_user_destino": target_user_id,
        "tipo_conta_destino": target_account_type,
    }
    data = str(data)
    client.send(data.encode())

    result_saque = client.recv(1024).decode()
    # fecha a conexão
    client.close()
    if result_saque != "Saque realizado com sucesso!":
        raise Exception(result_saque)
    else:
        return True, result_saque


def create_conta_corrente(id, password):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "07", "id": id, "senha": password}
    data = str(data)

    client.send(data.encode())

    current_account = client.recv(1024).decode()
    current_account = eval(current_account)
    current_account = ContaCorrente(
        current_account["id"],
        current_account["numero"],
        current_account["senha"],
        current_account["criacao"],
        current_account["saldo"],
        current_account["limite"],
    )
    return current_account


def create_conta_poupanca(id, password):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "08", "id": id, "senha": password}
    data = str(data)

    client.send(data.encode())

    savings_account = client.recv(1024).decode()
    savings_account = eval(savings_account)
    savings_account = ContaPoupanca(
        savings_account["id"],
        savings_account["numero"],
        savings_account["senha"],
        savings_account["criacao"],
        savings_account["saldo"],
    )
    return savings_account


def get_cliente_id_by_cpf(cpf):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "09", "cpf": cpf}
    data = str(data)
    client.send(data.encode())
    id = client.recv(1024).decode()
    if id == "False":
        return None
    else:
        return id


def deposito_conta_corrente(
    id,
    account_number,
    value,
    transfer=False,
    source_user_id=None,
    source_account_type=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "10",
        "id": id,
        "numero": account_number,
        "valor": value,
        "transferencia": transfer,
        "id_user_origem": source_user_id,
        "tipo_conta_origem": source_account_type,
    }
    data = str(data)
    client.send(data.encode())

    deposit_result = client.recv(1024).decode()
    # fecha a conexão
    client.close()
    if deposit_result != "Depósito realizado com sucesso!":
        raise Exception(deposit_result)
    else:
        return True, deposit_result


def deposito_conta_poupanca(
    id,
    account_number,
    value,
    transfer=False,
    source_user_id=None,
    source_account_type=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "11",
        "id": id,
        "numero": account_number,
        "valor": value,
        "transferencia": transfer,
        "id_user_origem": source_user_id,
        "tipo_conta_origem": source_account_type,
    }
    data = str(data)
    client.send(data.encode())

    result_deposito = client.recv(1024).decode()
    # fecha a conexão
    client.close()
    if result_deposito != "Depósito realizado com sucesso!":
        raise Exception(result_deposito)
    else:
        return True, result_deposito


def valida_senha_conta_corrente(id, password):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "12", "id": id, "senha": password}
    data = str(data)
    client.send(data.encode())
    validation = client.recv(1024).decode()
    if validation == "True":
        return True
    else:
        return False


def valida_senha_conta_poupanca(id, password):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "13", "id": id, "senha": password}
    data = str(data)
    client.send(data.encode())
    validation = client.recv(1024).decode()
    if validation == "True":
        return True
    else:
        return False
