# PyRPC

PyRPC is a simple RPC-framework written in Python. It supports simple and fast
access to remotely provided procedures by pickling (using the fast but
**in-secure** module cPickle, see below) all data (request/response) and
transporting it via TCP to the remote host.

Due to it's nature, cPickle is not intended to be secure. Under special
circumstances (e. g. malicious messages) remote executions might be possible.
Therefore you must ensure that the server is only reachable by trusted clients
in a secure and restricted environment (a public server is therefore absolutely
**not** recommended).

## Usage

Using PyRPC is pretty simple. See `client_example.py` for client-usage. The server
consists of two classes:

 * `RPCServer`
 * `RPCServerHandler`

`RPCServer` is used to manage all client connections; the `RPCServerHandler`
is newly instantiated for every request. It implements all provided procedures 
to the client; the method name is prefixed by `handle_`.

Every called method has access to the following instance attributes:

 * `address` - contains a (ip, port)-tuple of the remote client address
 * `data` - provides raw access to the request as a `dict`-object 

See `server_example.py` for corressponding server-usage.