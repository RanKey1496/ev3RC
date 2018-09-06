# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 00:13:09 2018

@author: Jhon GIl Sepulveda
"""

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import sys
import json

port = 8095
clients = []

class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        # self.sendMessage(self.data)
        print(json.loads(self.data))
        for client in clients:
            client.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        print(self.address, 'closed')
        clients.remove(self)

server = SimpleWebSocketServer('', port, SimpleEcho)
server.serveforever()