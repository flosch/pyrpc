# -*- coding: utf-8 -*-

import socket
import select

__all__ = ('Server', 'ServerException')

class Connection(object):

    def __init__(self, server, sock, address):
        self.server = server
        self.socket = sock
        self.address = address
        self.buffer_send = []
        self.buffer_read = []

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def handle_read(self):
        if not self.socket:
            # Connection not healthy, return!
            return False

        try:
            buf = self.socket.recv(8192)
        except socket.error:
            # Connection error
            return False
        
        if not buf:
            # No data available, connection probably closed
            self.disconnect()
            return False
        
        self.handle_data(buf)
        
        return True
    
    def handle_write(self):
        if not self.socket:
            # Connection not healthy, return!
            return False
        
        if not self.buffer_send:
            # Connection (presumedly) alive, but buffer empty! 
            return True
        
        buf = self.buffer_send[0]

        try:
            bytes_sent = self.socket.send(buf)
        except socket.error:
            # Connection error
            return False

        if bytes_sent >= len(buf):
            self.buffer_send = self.buffer_send[1:]
        else:
            self.buffer_send[0] = buf[bytes_sent:]
        
        return True
    
    def flush(self):
        for item in self.buffer_send:
            self.socket.sendall(item)
        self.buffer_send = [] 

    def send(self, buf):
        self.buffer_send.append(buf)

    def has_write(self):
        return len(self.buffer_send) > 0

class ServerException(Exception): pass
class Server(object):
    CONNECTION_CLASS = Connection
    
    def __init__(self, port, ip=''):
        self.ip = ip
        self.port = port
        self.socket = None
        
        self.clients = {} # fileno -> obj
    
    def start(self):
        self.stop()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(3)
    
    def stop(self):
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def _dispatch(self):
        removals = []
        for fno, cliobj in self.clients.iteritems():
            if not cliobj.socket:
                removals.append(fno)

        for removal in removals:
            del self.clients[removal]
                
        rl, wl, _ = select.select([self.socket.fileno(), ] + self.clients.keys(),
                                   map(lambda f: f.socket.fileno(), filter(lambda f: f.has_write(), self.clients.values())),
                                   [])

        for s in rl:
            if s == self.socket.fileno():
                # New client
                socket, address = self.socket.accept()
                self.clients[socket.fileno()] = self.CONNECTION_CLASS(server=self,
                                                                      sock=socket,
                                                                      address=address)
            else:
                if not self.clients[s].handle_read():
                    del self.clients[s]
        
        for s in wl:
            if self.clients.has_key(s) and not self.clients[s].handle_write():
                del self.clients[s]
    
    def run(self):
        self.start()
        try:
            while True:
                self._dispatch()
        finally:
            self.stop()