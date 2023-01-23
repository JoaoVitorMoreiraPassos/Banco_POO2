Blibliotecas instaladas: pyqt5, mysql-connector-python e Pillow.
Para executar a applicação é necessário criar um serivdor mysql ou compatível com o mysql-connector com os comando presentes no aquivo banco/msql/data.sql.
No arquivo banco/server/consultor.sql configure a conexão com o banco de acordo as suas definições.
No arquivo banco/server/server.py você pode configurar o ip e porta que o servidor irá utilizar.
No arquivo banco/client/client.py você direcionar a conexão para o endereço e pota onde o servidor está rodando.
Apóes seguir esses passos basta rodar o arquivo banco/index.py.
Lembre-se de exectuar a aplicação dentro do escopo da pasta banco.
