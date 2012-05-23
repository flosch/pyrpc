# -*- coding: utf-8 -*-

import zlib
import struct
import cPickle

class MessageException(Exception): pass
class MessageIncomplete(MessageException): pass
class MessageInvalid(MessageException): pass
class Message(object):
    MAGIC = 0x0815
    HEADER = "!HL"
    HEADER_SIZE = struct.calcsize(HEADER)
    
    def __init__(self, data, job_ident=None):
        self.data = data
    
    def __repr__(self):
        return '<Message data=%s>' % \
            (self.data, )

    def serialize(self):
        data = zlib.compress(cPickle.dumps(self.data))
        header = struct.pack(self.HEADER,
                             self.MAGIC,
                             len(data))
        return "".join([header, data])
    
    @staticmethod
    def parse(buf):
        if len(buf) < Message.HEADER_SIZE:
            raise MessageIncomplete(u'Header not present.')
        
        try:
            magic, datalen = struct.unpack(Message.HEADER, buf[:Message.HEADER_SIZE])
        except struct.error:
            raise MessageInvalid(u'Struct unpack failed.')
        
        buf = buf[Message.HEADER_SIZE:]
        
        if magic != Message.MAGIC:
            raise MessageInvalid(u'Invalid magic.')
        
        if len(buf) < datalen:
            raise MessageIncomplete(u'Data not complete.')
        
        try:
            data = cPickle.loads(zlib.decompress(buf[:datalen]))
        except ValueError:
            raise MessageInvalid(u'Deserialization failed.')
        except zlib.error:
            raise MessageInvalid(u'Decompress failed.')
    
        # What remains from the buffer?
        buf = buf[datalen:]
        
        return data, buf