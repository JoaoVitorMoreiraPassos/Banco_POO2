import threading

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, function):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        self.function = function
        print("[+] New thread started for ", clientAddress)

    def run(self):
        self.data = self.csocket.recv(1024).decode()
        if not self.data:
            return 
        
        self.data = eval(self.data)
        self.csocket.send(self.function(self.data))