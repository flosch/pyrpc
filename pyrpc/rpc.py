# -*- coding: utf-8 -*-

from client import Client, ClientException
from server import Server, Connection
from message import Message, MessageIncomplete, MessageInvalid

class RPCServerConnection(Connection):
    def __init__(self, *args, **kwargs):
        super(RPCServerConnection, self).__init__(*args, **kwargs)
        self.bufs = []
    
    def handle_data(self, buf):
        self.bufs.append(buf)
        
        while len(self.bufs) > 0:
            try:
                request, remaining_buf = Message.parse("".join(self.bufs))
            except MessageIncomplete:
                return True
            except MessageInvalid, e:
                raise ServerCommunicationError(e)
            
            self.bufs = [remaining_buf, ]
            
            fname = request['name']
            args = request['args']
            kwargs = request['kwargs']
            
            func_name = 'handle_%s' % fname
    
            if self.server.handler_kwargs:
                callee = self.server.handler(**self.server.handler_kwargs)
            else:
                callee = self.server.handler()
            callee.data = request
            callee.address = self.address
            callee.connection = self
            
            callee.prepare()
    
            if hasattr(callee, func_name):
                try:
                    result = getattr(callee, func_name)(*args, **kwargs)
                except Exception, e:
                    #raise # for debugging purposes
                    response = Message({
                        'status': 'exception',
                        'text': unicode(e)
                    })
                else:
                    response = Message({
                        'status': 'ok',
                        'result': result
                    })
            else:
                response = Message({
                    'status': 'notfound'
                })
            
            self.send(response.serialize())

class RPCServerHandler(object):
    
    def prepare(self):
        return

class RPCServerException(Exception): pass
class ServerCommunicationError(RPCServerException): pass
class RPCServer(Server):
    CONNECTION_CLASS = RPCServerConnection
    
    def __init__(self, *args, **kwargs):
        self.handler = kwargs.pop('handler')
        if kwargs.has_key('handler_kwargs'):
            self.handler_kwargs = kwargs.pop('handler_kwargs')
        else:
            self.handler_kwargs = None
        
        super(RPCServer, self).__init__(*args, **kwargs)

class RPCClientException(Exception): pass
class ClientCommunicationError(RPCClientException): pass
class RemoteException(RPCClientException): pass
class MethodNotFound(RPCClientException): pass
class RPCClient(Client):
    
    def __init__(self, env=None):
        super(RPCClient, self).__init__()
        self.env = env or {}
    
    def __getattr__(self, name):
        
        def do_call(*args, **kwargs):
            data = {
                'name': name,
                'args': args,
                'kwargs': kwargs,
            }
            data.update(self.env)
            request = Message(data)
            
            # Send request
            self.send(request.serialize())
            
            # Receive response
            bufs = []
            while True:
                try:
                    buf = self.recv()
                except ClientException, e:
                    raise ClientCommunicationError(e)
                
                if not buf:
                    raise ClientCommunicationError('Server hang up.')
                
                bufs.append(buf)
    
                try:
                    response, _ = Message.parse("".join(bufs))
                except MessageIncomplete:
                    continue
                except MessageInvalid, e:
                    raise ClientCommunicationError(e)
                else:
                    # Message complete
                    break
            
            if response.get('status') == 'exception':
                raise RemoteException(response.get('text'))
            elif response.get('status') == 'notfound':
                raise MethodNotFound(u'Method "%s" not found.' % name)
            elif response.get('status') == 'ok':
                return response.get('result')
            else:
                raise NotImplementedError
        
        return do_call