#!/usr/bin/python
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from OpenSSL import SSL

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.app import Application
from twisted.internet import ssl, reactor
from echoserv_ssl import ServerContextFactory
import sys

# TODO for some reason this raises an exception when run against an
# "nc -l -p 8000" (which seems to exit in the middle of the handshake).

#[tv@ki ..ork/twistedmatrix/Twisted/doc/examples]$ PYTHONPATH=~/work/twistedmatrix/Twisted python ./echoclient_ssl.py
#Installing SelectReactor, since unspecified.
#Starting factory <__main__.EchoClientFactory instance at 0x830c55c>
#Traceback (most recent call last):
#  File "/home/tv/work/twistedmatrix/Twisted/twisted/internet/default.py", line 528, in doSelect
#    why = getattr(selectable, method)()
#  File "/home/tv/work/twistedmatrix/Twisted/twisted/internet/tcp.py", line 220, in doConnect
#    self.socket.connect(self.realAddress)
#SSL.WantReadError: 
#closing socket
#Traceback (most recent call last):
#  File "/home/tv/work/twistedmatrix/Twisted/twisted/internet/default.py", line 539, in doSelect
#    selectable.connectionLost()
#  File "/home/tv/work/twistedmatrix/Twisted/twisted/internet/tcp.py", line 139, in connectionLost
#    protocol.connectionLost()
#exceptions.AttributeError: 'None' object has no attribute 'connectionLost'


class EchoClient(LineReceiver):
    end="Bye-bye!"
    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("What a fine day it is.")
        self.sendLine(self.end)

    def connectionLost(self):
        print 'connection lost (protocol)'
        reactor.stop()

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def connectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def connectionLost(self, connector):
        print 'connection lost'
        reactor.stop()

factory = EchoClientFactory()
reactor.connectSSL('localhost', 8000, factory, ssl.ClientContextFactory())
reactor.run()
