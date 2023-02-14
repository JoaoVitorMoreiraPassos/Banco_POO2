import threading


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, function):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        self.function = function
        print("[+] New thread started for ", clientAddress)

    def run(self):
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
