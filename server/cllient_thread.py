import threading


class ClientThread(threading.Thread):
    """
    Essa classe é responsável por criar uma thread para cada operação
    que se conecta ao servidor.
    
    ...
    
    Attributes
    ----------
    clientAddress : tuple
        Endereço do cliente.
    csocket : socket
        Socket do cliente.
    function : function
        Que será executada pela thread.
    
    Methods
    ---------
    run()
        Executa a função passada como parâmetro.
    
    """
    def __init__(self, clientAddress, clientsocket, function):
        """
        Constructs all the necessary attributes for the ClientThread object.

        Parameters
        ----------
            clientAddress : tuple
                Endereço do cliente.
            csocket : socket
                Socket do cliente.
            function : function
                que será executada pela thread.
        Returns
        -------
        None
        """
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        self.function = function
        print("[+] New thread started for ", clientAddress)

    def run(self):
        """
        Função que irá ser executada ao chamar o método start() da thread.
        Recebe os dados do cliente, executa a função passada como atributo da
        classe e envia a resposta para o cliente utilizando o socket passado
        como atributo da classe.

        Parameters
        ----------
        None
                    
        return
        ----------
        None
        """
        try:
            self.data = self.csocket.recv(1024).decode()
            if not self.data:
                return
            self.data = eval(self.data)
            sinc = threading.Lock()
            print(self.data)
            self.data = self.function(self.data, sinc)
            print(self.data)
            self.csocket.send(self.data)
        except Exception as e:
            print(e)
            self.csocket.send("False".encode())
            self.csocket.close()
