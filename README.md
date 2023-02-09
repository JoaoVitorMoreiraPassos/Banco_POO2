
# Projeto Banco - POO II

Projeto de um Banco, utilizando interface gráfica,
banco de dados e multithread, feita na matéria de Programação Orientada
a Objetos 2.

## Instalação

Crie um ambiente virtual python para o cliente e outro para o servidor:

```bash
  python3 -m venv venv
```
Ative o ambiente virtual:
```bash
  . venv/bin/activate
```
Instale as bibliotecas presentes no projeto:
```bash
  pip install -r requirements.txt
```

## Execução

- Para executar a applicação é necessário criar um servidor mysql ou compatível com o mysql-connector com os comando presentes no aquivo `banco/server/msql/data.sql.`

- No arquivo banco/server/consultor.sql configure a conexão com o banco de acordo as suas definições.

- No arquivo banco/server/server.py você pode configurar o ip e porta que o servidor irá utilizar.

- No arquivo banco/client/client.py você direcionar a conexão para o endereço e pota onde o servidor está rodando.

Após seguir esses passos basta rodar o seguinte comando:
```bash
  python index.py
```

Lembre-se de exectuar a aplicação dentro do escopo ou do server ou do client.
