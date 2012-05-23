# -*- coding: utf-8 -*-

import socket

__all__ = ('Client', 'ClientException')

class ClientException(Exception): pass
class Client(object):
    
    def __init__(self):
        self.socket = None
        self.address = None
    
    def connect(self, ip, port):
        self.disconnect()
        self.address = (ip, port)
        try:
            self.socket = socket.create_connection(self.address, timeout=2)
        except socket.error, e:
            raise ClientException(e)
    
    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def recv(self):
        try:
            return self.socket.recv(8192)
        except socket.error, e:
            raise ClientException(e)

    def send(self, buf):
        try:
            self.socket.sendall(buf)
        except socket.error, e:
            raise ClientException(e)