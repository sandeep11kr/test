import socket, os, random


class VirtualVpn:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ipaddr = socket.gethostbyname(self.hostname)
        self.localIP = self.ipaddr
        # localIP = "192.168.0.14"
        print('Local IP ',self.localIP)

    def disconnect(self):

        cmd = 'nordvpn -d'
        os.system(cmd)
        while self.ipaddr != self.localIP:
            self.ipaddr = socket.gethostbyname(self.hostname)
        print("Disconnected ", self.ipaddr)

    def connect(self):

        print('Connecting ', self.ipaddr)
        server = ['United States', 'India', 'Canada']

        cmd = 'nordvpn -c --group-name "{}"'.format(random.choice(server))
        os.system(cmd)
        while self.ipaddr == self.localIP:
            self.ipaddr = socket.gethostbyname(self.hostname)
        print("Connected ", self.ipaddr)
