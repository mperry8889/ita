#!/usr/bin/python

from errno import EBADF, EINTR, ECONNRESET
import socket
import select
import logging as log

from chatserver.client import Client as ChatClient
from chatserver.client import ERR
from chatserver.server import Server as ChatServer
from chatserver.command import ValidateCommand

log.basicConfig(level=log.DEBUG)

socklist = {}
serversock = None

port = 6668

def _logOut(sock):
    ChatServer.logout(socklist[sock].getNickname(), socklist[sock])

# set up the main listening socket
def _listen(port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.bind(('', port))
    fd.listen(512)
    fd.setblocking(False)
    return fd

# main entry point
def main():
    global serversock  # interpreter needs a hint here

    serversock = _listen(port)
    socklist[serversock] = 1
    
    while 1:
        loop()

# socket listening loop
def loop():
    while 1:
        try:
            read, write, error = select.select(socklist.keys(), [], [], 60)
            break
        
        # this happens if a client disconnects uncleanly
        except socket.error, e:
            if e.args[0] == EINTR:
                return
            elif e.args[0] == EBADF:
                # just select everything until one errors
                for sock in socklist:
                    try:
                        select.select([sock], [], [], 0)
                    except:
                        _logOut(sock)
                        socklist.pop(sock)
                        sock.close()
                        break
    try:                
        for sock in read:
            # on the listening server socket, accept new connections
            if sock.fileno() == serversock.fileno():
                client, address = sock.accept()
                client.setblocking(False)
                
                chatClient = ChatClient(client)
                socklist[client] = chatClient
                
            # handle regular input
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        # who sends 1KB of data to a chat server?
                        if len(data) == 1024:
                            _logOut(sock)
                            socklist.pop(sock)
                            sock.close()
                        if not ValidateCommand(data):
                            ERR(sock)
                        else:
                            socklist[sock].execute(data)
                    else:
                        _logOut(sock)
                        socklist.pop(sock)
                        sock.close()
                except socket.error, se:
                    if se.args[0] == ECONNRESET:
                        _logOut(sock)
                        socklist.pop(sock)
                        sock.close()
    
    # if the select() above fails, read/write/error will be invalid names, and the for
    # loop will throw an error.  ignore it and keep looping.                
    except NameError:
        pass


if __name__ == "__main__": main()