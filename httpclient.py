#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Abram Hindle, https://github.com/tywtyw2002, https://github.com/treedust, Mark Maligalig
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

DEFAULT_PORT = 80 # Use if port is not explicitly given

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        # Check if port is explictly written
        # Check for host; return host and port
        # (^\/\/|^@)?[a-zA-Z0-9.]+(^:|^\/)? to isolate parts of url
        #TODO: Clarify if host = www.google.com OR www.google.com/path
        #TODO: what about if host = [::1]?
        # Assuming every url starts with scheme://
        host_port = url.split("/")[2].split(":") # Get host:port
        host = host_port[0]

        if ":" in host_port:
            port = re.findall('', url)
        else:
            port = DEFAULT_PORT

        return host, port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open socket using IPv4 and TCP
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        # TODO: Do headers need to be stored in dict?
        headers = data.split("\r\n\r\n")[0]
        return headers

    def get_body(self, data):
        # TODO: Body = after headers?
        info = data.split("\r\n\r\n")
        body = None
        if len(info) > 1:
            body = info[1]
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        request = "GET \ HTTP/1.1\nHost: " + host + "\n\n"

        host, port = self.get_host_port(url)
        self.connect(host, port) # Connect to server
        self.sendall(request) # Send request to server

        self.socket.shutdown(socket.SHUT_WR) # Tell server socket is done sending!

        data = self.recvall(self.socket)
        #print(data) # User story 5

        print(self.get_headers(data))

        self.socket.close()



        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
