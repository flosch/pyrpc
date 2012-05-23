# -*- coding: utf-8 -*-

import time

from pyrpc import RPCClient

COUNT = 10000

def main():
    c = RPCClient()
    c.connect(ip='127.0.0.1', port=4711)
    
    print "5^2 + 10^2 =", c.pythagoras(5, 10)
    
    stime = time.time()
    for _ in xrange(COUNT):
        c.ping()
    etime = time.time()
    
    print "%d calls took %.2fs (%d/s)" % (COUNT, etime-stime, COUNT/(etime-stime))

if __name__ == "__main__":
    main()