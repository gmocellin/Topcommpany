#coding: utf-8

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from struct import unpack

class Echo (DatagramProtocol):
    def datagramReceived (self, data, (host, port)):
        seq, msg = unpack ('=I', data[:4])[0], data[4:]
        valores = msg.split ('|')
        nome, valores = valores[0], valores[1:]
        print "[%d] %r from %s" % (seq, ', '.join (valores), nome)

reactor.listenMulticast (10000, Echo (), listenMultiple = True)
reactor.run ()
