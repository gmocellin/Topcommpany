#coding: utf-8

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Echo (DatagramProtocol):
    def datagramReceived (self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        #self.transport.write (data, (host, port))

reactor.listenMulticast (10000, Echo (), listenMultiple = True)
reactor.run ()
