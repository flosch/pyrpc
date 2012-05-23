# -*- coding: utf-8 -*-

from pyrpc import RPCServer, RPCServerHandler

class CalcServerHandler(RPCServerHandler):
    
    def handle_pythagoras(self, a, b):
        return a**2 + b**2

    def handle_ping(self):
        return True

def main():
    cs = RPCServer(port=4711, handler=CalcServerHandler)
    try:
        cs.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()