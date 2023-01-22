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
    seguindo seguinte padrão: {"operacao": "01", "info_nessaria_para_a_operacao1": "inf1", "info_necessria_para_a_operacao2": "info2"} 
    será feita a identificação da operação desejada, com isso será realizada a conexão com o banco de dados através dos modulos
    do arquivo consultor_sql.py, e será retornado uma mensagem para o cliente, que será uma string no formato JSON
    de acordo com os dados retornados pelas funções axiliares que acessam o banco de dados.
"""


def do_login(email, senha):
    retorno = login(email, senha)
    if retorno[0]:
        contas = {}
        contas = retorno[1].contas
        if "cc" in contas.keys():
            contas["cc"] = {
                "id": contas["cc"].id,
                "numero": contas["cc"].numero,
                "senha": contas["cc"].senha,
                "criacao": contas["cc"].criacao,
                "saldo": contas["cc"].saldo,
                "limite": contas["cc"].limite,
            }
        if "cp" in contas.keys():
            contas["cp"] = {
                "id": contas["cp"].id,
                "numero": contas["cp"].numero,
                "senha": contas["cp"].senha,
                "criacao": contas["cp"].criacao,
                "saldo": contas["cp"].saldo,
            }
        user = f'{{"id": {retorno[1].id},"nome": "{retorno[1].nome}","cpf": "{retorno[1].cpf}","email": "{retorno[1].email}", "nascimento": "{retorno[1].nascimento}", "contas": {contas}}}'
        user = str(user)
        return True, user
    else:
        return False, None


def do_search_by_cpf(cpf, tipo):
    conta = busca_conta_por_cpf(cpf, tipo)
    if conta != None:
        if data["tipo"] == "cc":
            retorno = {
                "id": conta.id,
                "numero": conta.numero,
                "senha": conta.senha,
                "criacao": conta.criacao,
                "saldo": conta.saldo,
                "limite": conta.limite,
            }
        elif data["tipo"] == "cp":
            retorno = {
                "id": conta.id,
                "numero": conta.numero,
                "senha": conta.senha,
                "criacao": conta.criacao,
                "saldo": conta.saldo,
            }
        return retorno
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
            msg = con.recv(1024)
            # Se a mensagem for vazia, encerra a conexão
            if not msg:
                con.close()
                break
            # Decodifica a mensagem
            data = msg.decode()
            # Pega a string recebida e transforma em um dicionário
            data = eval(msg)
            # Pega o tipo de operação
            operacao = data["operacao"]
            # A partir daqui as operações serão identificadas e e realizadas
            if operacao == "01":
                # Operação de login
                # Faz a verificação do login
                result_login = do_login(data["email"], data["senha"])
                if result_login[0]:
                    con.send(result_login[1].encode())
                else:
                    con.send("False".encode())

            elif operacao == "02":
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

            elif operacao == "03":
                # Operação de busca de transações
                transations = get_transacoes(data["id"], data["tipo"])
                con.send(str(transations).encode())

            elif operacao == "04":
                # Operação de busca de conta por cpf
                retorno = do_search_by_cpf(data["cpf"], data["tipo"])
                if retorno != None:
                    con.send(str(retorno).encode())
                else:
                    con.send("False".encode())

            elif operacao == "05":
                # Operação de saque em uma conta corrente
                saque = None
                try:
                    saque = saque_conta_corrente(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_destino"],
                        data["tipo_conta_destino"],
                    )
                    if saque[0]:
                        con.send(saque[1].encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operacao == "06":
                # Operação de saque em uma conta poupança
                saque = None
                try:
                    saque = saque_conta_poupanca(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_destino"],
                        data["tipo_conta_destino"],
                    )
                    if saque[0]:
                        con.send(saque[1].encode())
                except Exception as E:
                    con.send(str(E).encode())
            elif operacao == "07":
                # Operação de criação de conta corrente
                conta = create_conta_corrente(data["id"], data["senha"])
                conta = {
                    "id": conta.id,
                    "numero": conta.numero,
                    "senha": conta.senha,
                    "criacao": conta.criacao,
                    "saldo": conta.saldo,
                    "limite": conta.limite,
                }
                con.send(str(conta).encode())
            elif operacao == "08":
                # Operação de criação de conta poupança
                conta = create_conta_poupanca(data["id"], data["senha"])
                conta = {
                    "id": conta.id,
                    "numero": conta.numero,
                    "senha": conta.senha,
                    "criacao": conta.criacao,
                    "saldo": conta.saldo,
                }
                con.send(str(conta).encode())
            elif operacao == "09":
                # Operação de busca de id de cliente por cpf
                id = get_cliente_id_by_cpf(data["cpf"])
                if id != None:
                    con.send(str(id).encode())
                else:
                    con.send("False".encode())

            elif operacao == "10":
                # Operação de depósito em uma conta corrente
                deposito = None
                try:
                    deposito = deposito_conta_corrente(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_origem"],
                        data["tipo_conta_origem"],
                    )
                    con.send(str(deposito[1]).encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operacao == "11":
                # Operação de depósito em uma conta poupança
                deposito = None
                try:
                    deposito = deposito_conta_poupanca(
                        data["id"],
                        data["numero"],
                        data["valor"],
                        data["transferencia"],
                        data["id_user_origem"],
                        data["tipo_conta_origem"],
                    )
                    con.send(str(deposito[1]).encode())
                except Exception as E:
                    con.send(str(E).encode())

            elif operacao == "12":
                # Operação de validação de senha de conta corrente
                validacao = valida_senha_conta_corrente(data["id"], data["senha"])
                if validacao:
                    con.send("True".encode())
                else:
                    con.send("False".encode())

            elif operacao == "13":
                # Operação de validação de senha de conta poupança
                validacao = valida_senha_conta_poupanca(data["id"], data["senha"])
                if validacao:
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
            break
