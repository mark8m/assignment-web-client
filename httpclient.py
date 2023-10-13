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
DEFAULT_PATH = "/" # Use if path is not explicitly given

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # Return host, port, path of given url
    def get_host_port_path(self,url):
        # Parse url, get host/port/path
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port
        path = parsed.path

        # Use default port or path if not given
        if port == None:
            port = DEFAULT_PORT
        if path == "":
            path = DEFAULT_PATH
        
        return host, port, path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open socket using IPv4 and TCP
        self.socket.connect((host, port))
        return None

    # Return response code
    def get_code(self, data):
        # Get first line of response, then code
        status_line = data.split("\r\n\r\n")[0].split("\r\n")[0]
        code = status_line.split(" ")[1]
        return int(code)

    # Returns headers in a dictionary
    def get_headers(self,data):
        headers = {}

        # Response code and headers together, separated by line
        code_headers = data.split("\r\n\r\n")[0].split("\r\n")
        
        # Headers separated into key/value pairs
        for i in range(1, len(code_headers)):
            header = code_headers[i].split(": ")
            key, value = header[0], header[1]
            headers[key] = value

        return headers

    # Return body of response, only if it exists
    def get_body(self, data):
        info = data.split("\r\n\r\n")
        body = ""
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

        host, port, path = self.get_host_port_path(url)
        request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"

        self.connect(host, port) # Connect to server
        self.sendall(request) # Send request to server

        response = self.recvall(self.socket)
        print(response) # User story 5

        self.close()

        code = self.get_code(response)
        body = self.get_body(response)

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
