blibliotecas instaladas: pyqt5, mysql-connector, mysql-connector-python e Pillow
para executar a applicação é necessário criar um serivdor mysql ou compatível com o mysql-connector com os comando presentes no aquivo banco/msql/data.sql.
no arquivo banco/server/consultor.sql configure a conexão com o banco de acordo as suas definições.
no arquivo banco/server/server.py você pode configurar o ip e porta que o servidor irá utilizar.
no arquivo banco/client/client.py você direcionar a conexão para o endereço e pota onde o servidor está rodando.
apóes seguir esses passos basta rodar o arquivo banco/index.py.
lembre-se de exectuar a aplicação dentro do escopo da pasta banco.
