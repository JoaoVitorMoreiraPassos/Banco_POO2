import mysql.connector as conex
from datetime import datetime
from bibs.cliente import Cliente
from bibs.conta import ContaCorrente, ContaPoupanca

banco = conex.connect(
    host="localhost", user="myuser", password="mypassword", database="mydb"
)   
    
def add_cliente(nome, cpf, nascimento, email, senha):
    cursor = banco.cursor()
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
        campo_duplicado = str(E).split("'")
        raise Exception(
            f"O {campo_duplicado[-2]} {campo_duplicado[1]} já está cadastrado!"
        )
    banco.commit()
    cursor.close()


def get_cliente_id_by_cpf(cpf):
    cursor = banco.cursor()
    result = cursor.execute("SELECT idcliente FROM cliente WHERE cpf = (%s)", (cpf,))
    print(result)
    result = cursor.fetchone()[0]
    return result


def login(email, senha):
    cursor = banco.cursor()
    cursor.execute(
        "SELECT * FROM cliente WHERE email = %s AND senha_acesso = MD5(%s)",
        (email, senha),
    )
    result = cursor.fetchone()
    if result:
        # 0 = id, 4 = nome, 1 = cpf, 2 = nascimento, 3 = email
        cliente = Cliente(result[0], result[4], result[1], result[2], result[3])
        cc = get_conta_corrente(cliente.id)
        cp = get_conta_poupanca(cliente.id)
        if cc:
            cliente.add_cc(cc)
        if cp:
            cliente.add_cp(cp)
        return True, cliente
    else:
        return False, None


def create_conta_corrente(id, senha):
    numero_de_contas = banco.cursor()
    numero_de_contas.execute("SELECT max(idconta_corrente) FROM conta_corrente")
    numero_de_contas = numero_de_contas.fetchone()
    if numero_de_contas[0] == None:
        numero_de_contas = (0,)
    numero_da_conta = numero_de_contas[0] + 100000

    cursor = banco.cursor()
    criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conta_corrente (numero, senha, cliente_idcliente, saldo, criacao, limite) VALUES (%s,MD5(%s), %s, %s, %s, %s)",
        (
            numero_da_conta,
            senha,
            id,
            0,
            criacao,
            800,
        ),
    )
    banco.commit()
    cursor = banco.cursor()
    cursor.execute(
        f"SELECT idconta_corrente FROM conta_corrente WHERE numero = {numero_da_conta}"
    )
    id_conta = cursor.fetchone()[0]

    conta = ContaCorrente(id_conta, numero_da_conta, senha, criacao, 0, 800)
    cursor.close()
    return conta


def create_conta_poupanca(id, senha):
    numero_de_contas = banco.cursor()
    numero_de_contas.execute("SELECT max(idconta_poupanca) FROM conta_poupanca")
    numero_de_contas = numero_de_contas.fetchone()
    if numero_de_contas[0] == None:
        numero_de_contas = (0,)
    cursor = banco.cursor()
    criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conta_poupanca (numero, senha, cliente_idcliente, saldo, criacao) VALUES (%s, MD5(%s), %s, %s, %s)",
        (
            int(numero_de_contas[0]) + 100000,
            senha,
            id,
            0,
            criacao,
        ),
    )
    banco.commit()
    cursor = banco.cursor()
    cursor.execute(
        f"SELECT idconta_poupanca FROM conta_poupanca WHERE numero = {int(numero_de_contas[0])+100000}"
    )
    id_conta = cursor.fetchone()[0]
    conta = ContaPoupanca(
        id_conta, int(numero_de_contas[0]) + 100000, senha, criacao, 0
    )
    cursor.close()
    return conta


def get_conta_corrente(id):
    print("entrou aqui")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_corrente WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    print("conta: ", result)
    try:
        result = result[0]
    except:
        return None
    try:
        # 0 = id, 1 = numero, 2 = senha, 3 = saldo, 4 = limite, 5 = criacao
        conta = ContaCorrente(
            result[0], result[1], result[2], result[5], result[3], result[4]
        )
    except:
        conta = None
    cursor.close()
    return conta


def get_conta_poupanca(id):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_poupanca WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    try:
        result = result[0]
    except:
        return None
    try:
        conta = ContaPoupanca(result[0], result[1], result[2], result[4], result[3])
    except:
        conta = None
    cursor.close()
    return conta


def valida_senha_conta_corrente(id, senha):
    cursor = banco.cursor()
    cursor.execute(
        "SELECT * FROM conta_corrente WHERE idconta_corrente = %s AND senha = MD5(%s)",
        (id, senha),
    )
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


def valida_senha_conta_poupanca(id, senha):
    cursor = banco.cursor()
    cursor.execute(
        "SELECT * FROM conta_poupanca WHERE idconta_poupanca = %s AND senha = MD5(%s)",
        (id, senha),
    )
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False


def add_transacao(id_da_conta, tipo_da_conta, valor, tipo):
    cursor = banco.cursor()
    if tipo_da_conta == "cc":
        cursor.execute(
            f"INSERT INTO historico (momento, tipo, valor, conta_corrente_idconta_corrente) VALUES ('{str(datetime.now()).split('.')[0]}', '{tipo}', '{valor}', '{id_da_conta}')"
        )
    else:
        cursor.execute(
            f"INSERT INTO historico (momento, tipo, valor, conta_poupanca_idconta_poupanca) VALUES ('{str(datetime.now()).split('.')[0]}', '{tipo}', '{valor}', '{id_da_conta}')"
        )

    banco.commit()
    cursor.close()


def get_transacoes(id_da_conta, tipo_da_conta):
    if isinstance(id_da_conta, tuple):
        id_da_conta = id_da_conta[0]
    cursor = banco.cursor()
    if tipo_da_conta == "cc":
        cursor.execute(
            f"SELECT * FROM historico WHERE conta_corrente_idconta_corrente = {id_da_conta}"
        )
    else:
        cursor.execute(
            f"SELECT * FROM historico WHERE conta_poupanca_idconta_poupanca = {id_da_conta}"
        )
    result = cursor.fetchall()
    cursor.close()
    return result


def deposito_conta_corrente(
    id, numero, valor, eh_transferencia=False, id_user_origem=None, tipo_origem=None
):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_corrente WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if valor <= 0:
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
        (result[0] + valor, numero),
    )
    if eh_transferencia:
        if tipo_origem == "cc":
            conta_origem = get_conta_corrente(id_user_origem)
        elif tipo_origem == "cp":
            conta_origem = get_conta_poupanca(id_user_origem)
        else:
            conta_origem = None
        id_user = cursor.execute(
            "SELECT cliente_idcliente FROM conta_corrente WHERE numero = %s", (numero,)
        )
        id_user = cursor.fetchone()[0]
        user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (id_user,)
        )
        user = cursor.fetchone()[0]
        add_transacao(
            id,
            "cc",
            valor,
            f"transferência realizada para conta {conta_origem.numero} de {user}",
        )
    else:
        add_transacao(id, "cc", valor, "deposito")
    banco.commit()
    cursor.close()
    return True, "Depósito realizado com sucesso!"


def deposito_conta_poupanca(
    id, numero, valor, eh_transferencia=False, id_user_origem=None, tipo_origem=None
):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_poupanca WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if valor <= 0:
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
        (result[0] + valor, numero),
    )
    if eh_transferencia:
        if tipo_origem == "cc":
            conta_origem = get_conta_corrente(id_user_origem)
        elif tipo_origem == "cp":
            conta_origem = get_conta_poupanca(id_user_origem)
        else:
            conta_origem = None

        id_user = cursor.execute(
            "SELECT cliente_idcliente FROM conta_corrente WHERE numero = %s", (numero,)
        )
        id_user = cursor.fetchone()[0]
        user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (id_user,)
        )
        user = cursor.fetchone()[0]
        add_transacao(
            id,
            "cp",
            valor,
            f"transferência recebida da conta {conta_origem.numero} de {user}",
        )
    else:
        add_transacao(id, "cp", valor, "deposito")
    banco.commit()
    cursor.close()
    return True, "Depósito realizado com sucesso!"


def saque_conta_corrente(
    id, numero, valor, eh_transferencia=False, id_user_destino=None, tipo_destino=None
):
    print("id", id, "numero", numero, "valor", valor, "eh_transferencia", eh_transferencia, "id_user_destino", id_user_destino, "tipo_destino", tipo_destino)
    cursor = banco.cursor()
    cursor.execute(
        "SELECT saldo, limite FROM conta_corrente WHERE numero = %s", (numero,)
    )
    result = cursor.fetchone()
    if result[1] < valor:
        cursor.close()
        raise Exception("Limite atingido!")
    if result[0] < valor:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if valor <= 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_corrente SET saldo = %s WHERE numero = %s",
        (result[0] - valor, numero),
    )
    if eh_transferencia:
        if tipo_destino == "cc":
            print("aqui")
            conta_destino = get_conta_corrente(id_user_destino)
        elif tipo_destino == "cp":
            print("aqui1")
            conta_destino = get_conta_poupanca(id_user_destino)
        else:
            print("aqui2")
            conta_destino = None
        print("conta destino: ", conta_destino)
        id_user = cursor.execute(
            "SELECT cliente_idcliente FROM conta_corrente WHERE numero = %s", (numero,)
        )
        id_user = cursor.fetchone()[0]
        user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (id_user,)
        )
        user = cursor.fetchone()[0]
        add_transacao(
            id,
            "cc",
            valor,
            f"transferência realizada para conta {conta_destino.numero} de {user}",
        )
    else:
        add_transacao(id, "cc", valor, "saque")
    banco.commit()
    cursor.close()
    return True, "Saque realizado com sucesso!"


def saque_conta_poupanca(
    id, numero, valor, eh_transferencia=False, id_user_destino=None, tipo_destino=None
):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_poupanca WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if result[0] < valor:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if valor <= 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute(
        "UPDATE conta_poupanca SET saldo = %s WHERE numero = %s",
        (result[0] - valor, numero),
    )
    if eh_transferencia:
        if tipo_destino == "cc":
            conta_destino = get_conta_corrente(id_user_destino)
        elif tipo_destino == "cp":
            conta_destino = get_conta_poupanca(id_user_destino)
        else:
            conta_destino = None
        id_user = cursor.execute(
            "SELECT cliente_idcliente FROM conta_corrente WHERE numero = %s", (numero,)
        )
        id_user = cursor.fetchone()[0]
        user = cursor.execute(
            "SELECT nome FROM cliente WHERE idcliente = %s", (id_user,)
        )
        user = cursor.fetchone()[0]
        add_transacao(
            id,
            "cp",
            valor,
            f"transferência realizada para conta {conta_destino.numero} de {user}",
        )
    else:
        add_transacao(id, "cp", valor, "saque")
    banco.commit()
    cursor.close()
    return True, "Saque realizado com sucesso!"


def busca_conta_por_cpf(cpf, tipo_da_conta):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente WHERE cpf = %s", (cpf,))
    try:
        id_user = cursor.fetchone()[0]
        cursor.close()
    except:
        return None
    if tipo_da_conta == "cc":
        return get_conta_corrente(id_user)
    else:
        return get_conta_poupanca(id_user)
