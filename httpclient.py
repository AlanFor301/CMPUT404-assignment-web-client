#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
'''
You left me paralized

but the only troppy you deserve is catastrophy

one day you know too much that heaven is a sin.
fade to black 
please fade fade fade to black 

every kiss got me crying 
because your eyes nose lips

they said time flies but you keep breaking its wings
after taht they show taht all that hell is all taht brings


you wish me well
you wish me well
I wish you hell

never want hear your voice again

let me go 
let me go

baby tell me please this is the end

tears got out of my mind

still got me crying 
i do crying 

'''
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    def connect(self, host, port):
	#new socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#connect to the host
        s.connect((host, port))

        return s

    def get_code(self, data):

	#print 'split by rnrn: '+data.split('\r\n\r\n')[1]
        return int(data.split(' ',2)[1])

    def get_headers(self,data):

        return data.split('\r\n\r\n')[0]

    def get_body(self, data):

        return data.split('\r\n\r\n',2)[1]

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):


        #use split to parse url
	urlparse = url.split('/')[2].split(':')
	hostName = urlparse[0]

	#handle regular urls without port number
	if len(urlparse) == 2:
		port = int(urlparse[1])		
		
	else:
		port = 80	
	#parse path
	path = url.split(hostName)[1].split('?')[0]

	#using socket conneting to the url
        s = self.connect(hostName, port)

	#writting a GET request string 
        message = "GET %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nConnection: close\r\n\r\n" % (path, hostName)
        s.send(message)
        response = self.recvall(s)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        if (args != None):
            Postcontent = urllib.urlencode(args)
        else:
            Postcontent = ""
        PostcontentLength = len(Postcontent)        

        #use split to parse url
	urlparse = url.split('/')[2].split(':')
	hostName = urlparse[0]

	#handle regular urls without port number
	if len(urlparse) == 2:
		port = int(urlparse[1])		
		
	else:
		port = 80	
	#parse path
	path = url.split(hostName)[1].split('?')[0]

	#using socket conneting to the url
        s = self.connect(hostName, port)  
      	message = "POST %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %d\r\n\r\n%s\r\n" % (path, hostName, PostcontentLength, Postcontent)
        s.send(message)
        message = self.recvall(s)
        code = self.get_code(message)
        body = self.get_body(message)
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
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
