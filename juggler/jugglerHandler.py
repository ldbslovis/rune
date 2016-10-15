#from http.server import HTTPServer, BaseHTTPRequestHandler
#from socketserver import ThreadingMixIn
#from urllib.parse import urlparse

import sys

from jugglerRequest import RuneRequest
from instanceManager import *

sys.path.insert(0, '../runeconnect')

from request import *
from handler import *


import json
import threading
import urllib


class JugglerHttpHandler(RuneHttpHandler):
    instManager = None

    def do_GET(self):
        print('GET REQUEST', self)

        info = self
        self.printClientInformation(info)
        self.pathParser(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        print('POST REQUEST', self)

        info = self
        self.printClientInformation(info)

        length = int(self.headers['Content-Length'])

        if self.headers['Content-Type'] == 'application/json':
            #print("json_data", self.rfile.read(length))
            post_data = self.decodeJsonRequest(self.rfile.read(length).decode('utf-8'))
        else:
            post_data = self.decodeDictRequest(self.rfile.read(length).decode('utf-8'))

        print("POST DATA:", post_data)

        #run instance manager
        self.instManager = InstanceManager()
        self.instManager.RunManager()
        self.instManager.ReceiveRequest(json.dumps(post_data),self)
 
        # reponse
        '''
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        '''
        return True


    def printClientInformation(self, info):
        print("client addr - ", info.client_address)
        print("command - ", info.command)
        print("request line - ", info.requestline)
        print("path - ", info.path)

    def pathParser(self, path):
        if path.endswith('/') == False :
            path += '/'
        
        splitResult = path.split('/')

        oldObject = None
        firstObject = None

        print("--- split result ---")
        print(splitResult)
        print("--- split result end ---")

        for data in splitResult:
            if data == '':
                continue
            parseResult =  RuneRequest(data)
            if( oldObject != None ):
                oldObject.addChild(parseResult)
            else:
                firstObject = parseResult
            oldObject = parseResult

        return firstObject

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == "__main__":
    #create server
    PORT = 8000
    server = ThreadedHTTPServer(('127.0.0.1', PORT), JugglerHttpHandler)
    print('Starting server, use <Ctrl-C> to stop')
    print('Waiting API call')
    server.serve_forever()

