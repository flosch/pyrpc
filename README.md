# PyRPC

PyRPC is a simple RPC-framework written in Python. It supports simple and fast
access to remotely provided procedures by pickling (using the fast but
**in-secure** module cPickle, see below) all data (request/response) and
transporting it via TCP to the remote host.

Due to it's nature, cPickle is not intended to be secure. Under special
cirmunstances (e. g. malicious messages) remote executions might be possible.
Therefore you must ensure that the server is only reachable by trusted clients
in a secure and restricted environment (a public server is therefore absolutely
**not** recommended).