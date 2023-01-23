import socket
import json
from consultor_sql import (
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
)

"""
    O serivdor irá receber uma mensagem do cliente, que é uma string no formato JSON.
    seguindo seguinte padrão: {"operacao": "01", "info_nessaria_para_a_operacao1": "info1", "info_necessria_para_a_operacao2": "info2"} 
    será feita a identificação da operação desejada, com isso será realizada a conexão com o banco de dados através dos modulos
    do arquivo consultor_sql.py, e será retornado uma mensagem para o cliente, que será uma string no formato JSON
    de acordo com os dados retornados pelas funções axiliares que acessam o banco de dados.
"""


def do_login(email, senha):
    # O retorno será um objeto do tipo Cliente
    authorization = login(email, senha)
    if authorization[0]:
        """As contas do cliente são objetos do tipo ContaCorrente ou ContaPoupanca que herdam do ojeto Conta
        Para enviar as informções para o cliente é necessário transformar os objetos em dicionários,
        para depois transformar em string e codifica-las em bytes.
        """
        accounts = {}
        accounts = authorization[1].contas
        if "cc" in accounts.keys():
            accounts["cc"] = {
                "id": accounts["cc"].id,
                "numero": accounts["cc"].numero,
                "senha": accounts["cc"].senha,
                "criacao": accounts["cc"].criacao,
                "saldo": accounts["cc"].saldo,
                "limite": accounts["cc"].limite,
            }
        if "cp" in accounts.keys():
            accounts["cp"] = {
                "id": accounts["cp"].id,
                "numero": accounts["cp"].numero,
                "senha": accounts["cp"].senha,
                "criacao": accounts["cp"].criacao,
                "saldo": accounts["cp"].saldo,
            }
        # Empacota as informações do cliente e das contas em um dicionário e retorna como string
        user = f'{{"id": {authorization[1].id},"nome": "{authorization[1].nome}","cpf": "{authorization[1].cpf}","email": "{authorization[1].email}", "nascimento": "{authorization[1].nascimento}", "contas": {accounts}}}'
        user = str(user)
        return True, user
    else:
        return False, None


def do_search_by_cpf(cpf, account_type):
    # O retorno será um objeto do tipo ContaCorrente ou ContaPoupanca que herdam do ojeto Conta
    """
    Para enviar as informções para o cliente é necessário transformar os objetos em dicionários,
    para depois transformar em string e codifica-las em bytes.
    """
    account = busca_conta_por_cpf(cpf, account_type)
    if account != None:
        if account_type == "cc":
            account = {
                "id": account.id,
                "numero": account.numero,
                "senha": account.senha,
                "criacao": account.criacao,
                "saldo": account.saldo,
                "limite": account.limite,
            }
        elif account_type == "cp":
            account = {
                "id": account.id,
                "numero": account.numero,
                "senha": account.senha,
                "criacao": account.criacao,
                "saldo": account.saldo,
            }
        return account
    return None


host = "0.0.0.0"
port = 50000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

while True:
    # Faz o servidor aguardar por uma conexão
    con, ende = server.accept()
    while True:
        # Faz o servidor aguardar por uma mensagem
        try:
            # Recebe a mensagem do cliente
            request = con.recv(1024)
            # Se a mensagem for vazia, encerra a conexão
            if not request:
                con.close()
                break
            # Decodifica a mensagem
            data = request.decode()
            # Pega a string recebida e transforma em um dicionário
            data = eval(request)
            # Pega o tipo de operação
            operation = data["operacao"]
            # A partir daqui as operações serão identificadas e e realizadas
            if operation == "01":
                # Operação de login
                # Faz a verificação do login
                result_login = do_login(data["email"], data["senha"])
                if result_login[0]:
                    con.send(result_login[1].encode())
                else:
                    con.send("False".encode())

            elif operation == "02":
                # Operação de cadastro
                try:
                    add_cliente(
                        data["nome"],
                        data["cpf"],
                        data["nascimento"],
                        data["email"],
                        data["senha"],
                    )
                    con.send("True".encode())
                except Exception as E:
                    con.send("False".encode())

            elif operation == "03":
                # Operação de busca de transações
                transactions = get_transacoes(data["id"], data["tipo"])
                con.send(str(transactions).encode())

            elif operation == "04":
                # Operação de busca de conta por cpf
                account = do_search_by_cpf(data["cpf"], data["tipo"])
                if account != None:
                    con.send(str(account).encode())
                else:
                    con.send("False".encode())

            elif operation == "05":
                # Operação de saque em uma conta corrente
                withdraw_result = None
                try:
                    withdraw_result = saque_conta_corrente(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_destino"],
                        data["tipo_conta_destino"],
                    )
                    if withdraw_result[0]:
                        con.send(withdraw_result[1].encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operation == "06":
                # Operação de saque em uma conta poupança
                withdraw_result = None
                try:
                    withdraw_result = saque_conta_poupanca(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_destino"],
                        data["tipo_conta_destino"],
                    )
                    if withdraw_result[0]:
                        con.send(withdraw_result[1].encode())
                except Exception as E:
                    con.send(str(E).encode())
            elif operation == "07":
                # Operação de criação de conta corrente
                account = create_conta_corrente(data["id"], data["senha"])
                account = {
                    "id": account.id,
                    "numero": account.numero,
                    "senha": account.senha,
                    "criacao": account.criacao,
                    "saldo": account.saldo,
                    "limite": account.limite,
                }
                con.send(str(account).encode())
            elif operation == "08":
                # Operação de criação de conta poupança
                account = create_conta_poupanca(data["id"], data["senha"])
                account = {
                    "id": account.id,
                    "numero": account.numero,
                    "senha": account.senha,
                    "criacao": account.criacao,
                    "saldo": account.saldo,
                }
                con.send(str(account).encode())
            elif operation == "09":
                # Operação de busca de id de cliente por cpf
                id = get_cliente_id_by_cpf(data["cpf"])
                if id != None:
                    con.send(str(id).encode())
                else:
                    con.send("False".encode())

            elif operation == "10":
                # Operação de depósito em uma conta corrente
                try:
                    deposit_result = deposito_conta_corrente(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_origem"],
                        data["tipo_conta_origem"],
                    )
                    con.send(str(deposit_result[1]).encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operation == "11":
                # Operação de depósito em uma conta poupança
                try:
                    deposit_result = deposito_conta_poupanca(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_origem"],
                        data["tipo_conta_origem"],
                    )
                    con.send(str(deposit_result[1]).encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operation == "12":
                # Operação de validação de senha de conta corrente
                validation = valida_senha_conta_corrente(data["id"], data["senha"])
                if validation:
                    con.send("True".encode())
                else:
                    con.send("False".encode())

            elif operation == "13":
                # Operação de validação de senha de conta poupança
                validation = valida_senha_conta_poupanca(data["id"], data["senha"])
                if validation:
                    con.send("True".encode())
                else:
                    con.send("False".encode())

        except KeyboardInterrupt:
            con.close()
            server.close()
            quit()
        except Exception as E:
            con.close()
            server.close()
            quit()
