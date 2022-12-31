import mysql.connector as conex
from bibs.cliente import Cliente
from bibs.conta import ContaCorrente, ContaPoupanca
from datetime import datetime

banco = conex.connect(
    host="localhost",
    user="root",
    passwd="",
    database="mydb"
)

def get_columns(table):
    global banco
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    columns = [column[0] for column in cursor.description]
    return columns

def add_cliente(nome, cpf, nascimento, email, senha):
    cursor = banco.cursor()
    try:
        cursor.execute("INSERT INTO cliente (cpf, nascimento, email, nome, senha_acesso) VALUES (%s, %s, %s, %s, %s)", (cpf, nascimento,email,nome, senha))
    except Exception as E:
        campo_duplicado = str(E).split("'")
        raise Exception(f"O {campo_duplicado[-2]} {campo_duplicado[1]} já está cadastrado!")
    banco.commit()
    cursor.close()
    
def login(email, senha):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente WHERE email = %s AND senha_acesso = %s", (email, senha))
    result = cursor.fetchone()
    if result:
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
    if(numero_de_contas[0] == None): numero_de_contas = (0,)
    cursor = banco.cursor()
    cursor.execute("INSERT INTO conta_corrente (numero, senha, cliente_idcliente, saldo, limite) VALUES (%s, %s, %s, %s, %s)", (int(numero_de_contas[0])+100000, senha, id, 0, 800))
    banco.commit()
    cursor = banco.cursor()
    num = int(numero_de_contas[0])+100000
    cursor.execute(f"SELECT idconta_corrente FROM conta_corrente WHERE numero = {num}")
    id_conta = cursor.fetchone()[0]
    conta = ContaCorrente(id_conta, int(numero_de_contas[0])+100000, senha, 0, 800)
    cursor.close()
    return conta
    

def create_conta_poupanca(id, senha):
    numero_de_contas = banco.cursor()
    numero_de_contas.execute("SELECT max(idconta_poupanca) FROM conta_poupanca") 
    numero_de_contas = numero_de_contas.fetchone()
    if(numero_de_contas[0] == None): numero_de_contas = (0,)
    cursor = banco.cursor()
    cursor.execute("INSERT INTO conta_poupanca (numero, senha, cliente_idcliente, saldo) VALUES (%s, %s, %s, %s)", (int(numero_de_contas[0])+100000, senha, id, 0))
    banco.commit()
    cursor = banco.cursor()
    cursor.execute(f"SELECT idconta_poupanca FROM conta_poupanca WHERE numero = {int(numero_de_contas[0])+100000}")
    id_conta = cursor.fetchone()[0]
    conta = ContaPoupanca(id_conta, int(numero_de_contas[0])+100000, senha, 0)
    cursor.close()
    return conta
    
def get_conta_corrente(id):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_corrente WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    try:
        conta = ContaCorrente(result[0][0],result[0][1], result[0][5], result[0][3], result[0][4])
    except:
        conta = None
    cursor.close()
    return conta

def get_conta_poupanca(id):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_poupanca WHERE cliente_idcliente = %s", (id,))
    result = cursor.fetchall()
    try:
        conta = ContaPoupanca(result[0][0], result[0][1], result[0][2], result[0][3])
    except:
        conta = None
    cursor.close()
    return conta

def valida_senha_conta_corrente(id, senha):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_corrente WHERE idconta_corrente = %s AND senha = %s", (id, senha))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False
    
def valida_senha_conta_poupanca(id, senha):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM conta_poupanca WHERE idconta_poupanca = %s AND senha = %s", (id, senha))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False

def add_transacao(id_da_conta, tipo_da_conta, valor, tipo):
    cursor = banco.cursor()
    if tipo_da_conta == "cc":
        cursor.execute(f"INSERT INTO historico (momento, tipo, valor, conta_corrente_idconta_corrente) VALUES ('{str(datetime.now()).split('.')[0]}', '{tipo}', '{valor}', '{id_da_conta}')")
    else:
        cursor.execute(f"INSERT INTO historico (momento, tipo, valor, conta_poupanca_idconta_poupanca) VALUES ('{str(datetime.now()).split('.')[0]}', '{tipo}', '{valor}', '{id_da_conta}')")
        
    banco.commit()
    cursor.close()

def get_transacoes(id_da_conta, tipo_da_conta):
    if isinstance(id_da_conta, tuple):
        id_da_conta = id_da_conta[0]
    cursor = banco.cursor()
    if tipo_da_conta ==  "cc":
        cursor.execute(f"SELECT * FROM historico WHERE conta_corrente_idconta_corrente = {id_da_conta}")
    else: 
        cursor.execute(f"SELECT * FROM historico WHERE conta_poupanca_idconta_poupanca = {id_da_conta}")
    result = cursor.fetchall()
    cursor.close()
    return result

def deposito_conta_corrente(id, numero, valor, eh_transacao=False):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_corrente WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if valor < 0:
        raise Exception("Valor inválido!")
    cursor.execute("UPDATE conta_corrente SET saldo = %s WHERE numero = %s", (result[0] + valor, numero))
    banco.commit()
    cursor.close()
    add_transacao(id,"cc",valor, "deposito" if not eh_transacao else "transferência recebida")
    return True, "Depósito realizado com sucesso!"

def deposito_conta_poupanca(id, numero, valor, eh_transferencia=False):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_poupanca WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if valor < 0:
        raise Exception("Valor inválido!")
    cursor.execute("UPDATE conta_poupanca SET saldo = %s WHERE numero = %s", (result[0] + valor, numero))
    banco.commit()
    cursor.close()
    add_transacao(id,"cp",valor, "deposito" if not eh_transferencia else "transferência recebida")
    return True, "Depósito realizado com sucesso!"

def saque_conta_corrente(id, numero, valor, eh_transacao=False):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo, limite FROM conta_corrente WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if result[1] < valor:
        cursor.close()
        raise Exception("Limite atingido!")
    if result[0] < valor:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if valor < 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute("UPDATE conta_corrente SET saldo = %s WHERE numero = %s", (result[0] - valor, numero))
    banco.commit()
    cursor.close()
    add_transacao(id, "cc", valor, "saque" if not eh_transacao else "transferencia realizada")
    cursor.close()
    return True, "Saque realizado com sucesso!"

def saque_conta_poupanca(id, numero, valor, eh_transacao=False):
    cursor = banco.cursor()
    cursor.execute("SELECT saldo FROM conta_poupanca WHERE numero = %s", (numero,))
    result = cursor.fetchone()
    if result[0] < valor:
        cursor.close()
        raise Exception("Saldo insuficiente!")
    if valor < 0:
        cursor.close()
        raise Exception("Valor inválido!")
    cursor.execute("UPDATE conta_poupanca SET saldo = %s WHERE numero = %s", (result[0] - valor, numero))
    banco.commit()
    cursor.close()
    add_transacao(id, "cp", valor, "saque" if not eh_transacao else "transferencia realizada")
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
    