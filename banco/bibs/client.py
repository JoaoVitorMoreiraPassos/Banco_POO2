import socket
import datetime
from bibs.cliente import Cliente
from bibs.conta import ContaCorrente, ContaPoupanca

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
    port = 50000

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))

    return cliente


def login(email, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "01", "email": email, "senha": senha}
    data = str(data)
    client.send(data.encode())
    result_login = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se o login foi bem sucedido
    if result_login == "False":
        return False, None
    else:
        # Transforma o resultado em um objeto Cliente
        user = eval(result_login)
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


def add_cliente(nome, cpf, nascimento, email, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "02",
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "email": email,
        "senha": senha,
    }
    data = str(data)
    client.send(data.encode())
    result_add = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se o cadastro foi bem sucedido e retorna o resultado para o usuário
    if result_add == "False":
        raise Exception("Erro ao adicionar cliente")
    else:
        return True, None


def get_transacoes(id, tipo):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "03", "id": id, "tipo": tipo}
    data = str(data)
    client.send(data.encode())
    result_transacoes = client.recv(2048).decode()
    # Fecha a conexão
    client.close()
    # Verifica se a busca por transações foi bem sucessida e retorna o resultado para o usuário
    if result_transacoes == "False":
        raise Exception("Erro ao adicionar cliente")
    else:
        return eval(result_transacoes)


def busca_conta_por_cpf(cpf, tipo_da_conta):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "04", "cpf": cpf, "tipo": tipo_da_conta}
    data = str(data)
    client.send(data.encode())
    result_contas = client.recv(1024).decode()
    # Fecha a conexão
    client.close()
    # Verifica se a busca por transações foi bem sucessida e retorna o resultado para o usuário
    if result_contas == "False":
        return None
    else:
        conta = eval(result_contas)
        if tipo_da_conta == "cc":
            conta = ContaCorrente(
                conta["id"],
                conta["numero"],
                conta["senha"],
                conta["criacao"],
                conta["saldo"],
                conta["limite"],
            )
        elif tipo_da_conta == "cp":
            conta = ContaPoupanca(
                conta["id"],
                conta["numero"],
                conta["senha"],
                conta["criacao"],
                conta["saldo"],
            )
        # print(conta.id, conta.numero, conta.senha, conta.criacao, conta.saldo)
        return conta


def saque_conta_corrente(
    id,
    numero,
    valor,
    transferencia=False,
    id_user_destino=None,
    tipo_conta_destino=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "05",
        "id": id,
        "numero": numero,
        "valor": valor,
        "transferencia": transferencia,
        "id_user_destino": id_user_destino,
        "tipo_conta_destino": tipo_conta_destino,
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


def saque_conta_poupanca(
    id,
    numero,
    valor,
    transferencia=False,
    id_user_destino=None,
    tipo_conta_destino=None,
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "06",
        "id": id,
        "numero": numero,
        "valor": valor,
        "transferencia": transferencia,
        "id_user_destino": id_user_destino,
        "tipo_conta_destino": tipo_conta_destino,
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


def create_conta_corrente(id, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "07", "id": id, "senha": senha}
    data = str(data)

    client.send(data.encode())

    conta_corrente = client.recv(1024).decode()
    conta_corrente = eval(conta_corrente)
    conta_corrente = ContaCorrente(
        conta_corrente["id"],
        conta_corrente["numero"],
        conta_corrente["senha"],
        conta_corrente["criacao"],
        conta_corrente["saldo"],
        conta_corrente["limite"],
    )
    return conta_corrente


def create_conta_poupanca(id, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "08", "id": id, "senha": senha}
    data = str(data)

    client.send(data.encode())

    conta_poupanca = client.recv(1024).decode()
    conta_poupanca = eval(conta_poupanca)
    conta_poupanca = ContaPoupanca(
        conta_poupanca["id"],
        conta_poupanca["numero"],
        conta_poupanca["senha"],
        conta_poupanca["criacao"],
        conta_poupanca["saldo"],
    )
    return conta_poupanca


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
    id, numero, valor, transferencia=False, id_user_origem=None, tipo_conta_origem=None
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "10",
        "id": id,
        "numero": numero,
        "valor": valor,
        "transferencia": transferencia,
        "id_user_origem": id_user_origem,
        "tipo_conta_origem": tipo_conta_origem,
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


def deposito_conta_poupanca(
    id, numero, valor, transferencia=False, id_user_origem=None, tipo_conta_origem=None
):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {
        "operacao": "11",
        "id": id,
        "numero": numero,
        "valor": valor,
        "transferencia": transferencia,
        "id_user_origem": id_user_origem,
        "tipo_conta_origem": tipo_conta_origem,
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


def valida_senha_conta_corrente(id, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "12", "id": id, "senha": senha}
    data = str(data)
    client.send(data.encode())
    validacao = client.recv(1024).decode()
    if validacao == "True":
        return True
    else:
        return False


def valida_senha_conta_poupanca(id, senha):
    # Faz a conexão com o servidor
    client = connect()
    # Envia os dados para o servidor e recebe a resposta
    data = {"operacao": "13", "id": id, "senha": senha}
    data = str(data)
    client.send(data.encode())
    validacao = client.recv(1024).decode()
    if validacao == "True":
        return True
    else:
        return False
