import socket
from client_thread import ClientThread
from sql_queries import (
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

"""
    O serivdor irá receber uma mensagem do cliente, que é uma string no formato JSON.
    seguindo seguinte padrão: {"operacao": "01", "info_nessaria_para_a_operacao1": "info1", "info_necessria_para_a_operacao2": "info2"} 
    será feita a identificação da operação desejada, com isso será realizada a conexão com o banco de dados através dos modulos
    do arquivo consultor_sql.py, e será retornado uma mensagem para o cliente, que será uma string no formato JSON
    de acordo com os dados retornados pelas funções axiliares que acessam o banco de dados.
"""


def do_login(email, password):
    """
    Busca a credenciais passadas pelo cliente no banco de dados. e autentica o
    cliente.

            Parameters:
                    email (str): email do cliente
                    password (str): senha do cliente
            Returns:
                    (bool, Cliente): True e um objeto do tipo Cliente,
                    caso o login seja bem sucedido,
    """
    # O retorno será um objeto do tipo Cliente
    authorization = login(email, password)
    if authorization[0]:
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
    """
    Busca uma conta no banco de dados, a partir do cpf do cliente
    e do tipo da conta.

            Parameters:
                    cpf (str): cpf do cliente
                    account_type (str): tipo da conta
            Returns:
                    (dict): dicionário com as informações da conta
    """
    account = busca_conta_por_cpf(cpf, account_type)
    if account is not None:
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


def manager_operations(data, sinc):
    """
    Gerencia as operações que serão realizadas pelo servidor,
    de acordo com a operação.

            Parameters:
                    data (dict): dicionário com as informações da operação.
                    sinc (threading.Semaphore): semáforo para sincronizar
                    o acesso ao banco de dados.
            Returns:
                    (str): string codificada com as informações da operação.
    """
    operation = data["operacao"]
    if operation == "01":
        # Operação de login
        # Faz a verificação do login
        sinc.acquire()
        result_login = do_login(data["email"], data["senha"])
        sinc.release()
        if result_login[0]:
            print(f"Um cliente entrou.")
            return (result_login[1].encode())
        else:
            return ("False".encode())

    elif operation == "02":
        # Operação de cadastro
        try:
            sinc.acquire()
            add_cliente(
                data["nome"],
                data["cpf"],
                data["nascimento"],
                data["email"],
                data["senha"],
            )
            sinc.release()
            print("Um novo cliente foi cadastrado")
            return ("True".encode())
        except Exception:
            return ("False".encode())

    elif operation == "03":
        # Operação de busca de transações
        sinc.acquire()
        transactions = get_transacoes(data["id"], data["tipo"])
        sinc.release()
        return (str(transactions).encode())

    elif operation == "04":
        # Operação de busca de conta por cpf
        sinc.acquire()
        account = do_search_by_cpf(data["cpf"], data["tipo"])
        sinc.release()
        if account != None:
            return (str(account).encode())
        else:
            return ("False".encode())

    elif operation == "05":
        # Operação de saque em uma conta corrente
        withdraw_result = None
        try:
            sinc.acquire()
            withdraw_result = saque_conta_corrente(
                data["id"],
                data["numero"],
                data["valor"],
                data["transferencia"],
                data["id_user_destino"],
                data["tipo_conta_destino"],
            )
            sinc.release()
            if withdraw_result[0]:
                if data["transferencia"]:
                    print("Transferencia realizada")
                else:
                    print("Saque realizado")
                return (withdraw_result[1].encode())
        except Exception as E:
            return (str(E).encode())

    elif operation == "06":
        # Operação de saque em uma conta poupança
        withdraw_result = None
        try:
            sinc.acquire()
            withdraw_result = saque_conta_poupanca(
                data["id"],
                data["numero"],
                data["valor"],
                data["transferencia"],
                data["id_user_destino"],
                data["tipo_conta_destino"],
            )
            sinc.release()
            if withdraw_result[0]:
                if data["transferencia"]:
                    print("Transferencia realizada")
                else:
                    print("Saque realizado")
                return (withdraw_result[1].encode())
        except Exception as E:
            return (str(E).encode())
    elif operation == "07":
        # Operação de criação de conta corrente
        sinc.acquire()
        account = create_conta_corrente(data["id"], data["senha"])
        sinc.release()
        account = {
            "id": account.id,
            "numero": account.numero,
            "senha": account.senha,
            "criacao": account.criacao,
            "saldo": account.saldo,
            "limite": account.limite,
        }
        print("Conta corrente criada")
        return (str(account).encode())
    elif operation == "08":
        # Operação de criação de conta poupança
        sinc.acquire()
        account = create_conta_poupanca(data["id"], data["senha"])
        sinc.release()
        account = {
            "id": account.id,
            "numero": account.numero,
            "senha": account.senha,
            "criacao": account.criacao,
            "saldo": account.saldo,
        }
        print("Conta poupanca criada")
        return (str(account).encode())
    elif operation == "09":
        # Operação de busca de id de cliente por cpf
        sinc.acquire()
        id = get_cliente_id_by_cpf(data["cpf"])
        sinc.release()
        if id != None:
            return (str(id).encode())
        else:
            return ("False".encode())

    elif operation == "10":
        # Operação de depósito em uma conta corrente
        try:
            sinc.acquire()
            deposit_result = deposito_conta_corrente(
                data["id"],
                data["numero"],
                data["valor"],
                data["transferencia"],
                data["id_user_origem"],
                data["tipo_conta_origem"],
            )
            sinc.release()
            return (str(deposit_result[1]).encode())
        except Exception as E:
            return (str(E).encode())

    elif operation == "11":
        # Operação de depósito em uma conta poupança
        try:
            sinc.acquire()
            deposit_result = deposito_conta_poupanca(
                data["id"],
                data["numero"],
                data["valor"],
                data["transferencia"],
                data["id_user_origem"],
                data["tipo_conta_origem"],
            )
            sinc.release()
            return (str(deposit_result[1]).encode())
        except Exception as E:
            return (str(E).encode())

    elif operation == "12":
        # Operação de validação de senha de conta corrente
        sinc.acquire()
        validation = valida_senha_conta_corrente(
            data["id"], data["senha"]
        )
        sinc.release()
        if validation:
            return ("True".encode())
        else:
            return ("False".encode())

    elif operation == "13":
        # Operação de validação de senha de conta poupança
        sinc.acquire()
        validation = valida_senha_conta_poupanca(
            data["id"], data["senha"]
        )
        sinc.release()
        if validation:
            return ("True".encode())
        else:
            return ("False".encode())
    elif operation == "14":
        """Busca um usuário pelo id"""
        sinc.acquire()
        user = get_user_by_id(data["id"])
        sinc.release()
        if user:
            accounts = user.contas
            if "cc" in accounts:
                accounts["cc"] = {
                    "id": accounts["cc"].id,
                    "numero": accounts["cc"].numero,
                    "senha": accounts["cc"].senha,
                    "criacao": accounts["cc"].criacao,
                    "saldo": accounts["cc"].saldo,
                    "limite": accounts["cc"].limite,
                }
            if "cp" in accounts:
                accounts["cp"] = {
                    "id": accounts["cp"].id,
                    "numero": accounts["cp"].numero,
                    "senha": accounts["cp"].senha,
                    "criacao": accounts["cp"].criacao,
                    "saldo": accounts["cp"].saldo,
                }

            user = f'{{"id": {user.id},"nome": "{user.nome}","cpf": "{user.cpf}","email": "{user.email}", "nascimento": "{user.nascimento}", "contas": {accounts}}}'
            user = str(user)
            return user.encode()
        else:
            return "False".encode()


def start():
    """
    Inicia e gerencia o servidor.

            Parameters:
                    None
            Returns:
                    None
    """
    host = "0.0.0.0"
    port = 50002
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    while True:
        # Faz o servidor aguardar por uma conexão
        clientsock, clientAddress = server.accept()
        try:
            newthread = ClientThread(
                clientAddress, clientsock, manager_operations)
            newthread.start()

        except KeyboardInterrupt:
            clientsock.close()
            server.close()
            # quit()
        except Exception as E:
            print("erro de conexão: ", E)
            clientsock.close()
            server.close()
        # quit()


if __name__ == "__main__":
    start()
