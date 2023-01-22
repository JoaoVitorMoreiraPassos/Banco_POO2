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
    con, ende = server.accept()
    while True:
        try:
            msg = con.recv(1024)
            if not msg:
                con.close()
                break
            data = msg.decode()
            data = eval(msg)
            operacao = data["operacao"]
            if operacao == "01":
                result_login = do_login(data["email"], data["senha"])
                if result_login[0]:
                    con.send(result_login[1].encode())
                else:
                    con.send("False".encode())

            elif operacao == "02":
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
                transations = get_transacoes(data["id"], data["tipo"])
                con.send(str(transations).encode())

            elif operacao == "04":
                retorno = do_search_by_cpf(data["cpf"], data["tipo"])
                if retorno != None:
                    con.send(str(retorno).encode())
                else:
                    con.send("False".encode())

            elif operacao == "05":
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
                id = get_cliente_id_by_cpf(data["cpf"])
                if id != None:
                    con.send(str(id).encode())
                else:
                    con.send("False".encode())

            elif operacao == "10":
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
                validacao = valida_senha_conta_corrente(data["id"], data["senha"])
                if validacao:
                    con.send("True".encode())
                else:
                    con.send("False".encode())

            elif operacao == "13":
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
