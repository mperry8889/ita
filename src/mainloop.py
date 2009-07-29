from errno import EBADF
import socket
import select
import sys
import logging as log

from chatserver.client import Client as ChatClient
from chatserver.client import ACK, ERR, State
from chatserver.server import Server as ChatServer
from chatserver.command import ValidateCommand

log.basicConfig(level=log.DEBUG)

read_socks = {}
ignore_socks = {}
serversock = None

port = 6668

server = ChatServer

def _logOut(sock):
    ChatServer.logout(read_socks[sock].getNickname(), read_socks[sock])

# set up the main listening socket
def _listen(port):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.bind(('', port))
    fd.listen(5)
    fd.setblocking(False)
    return fd

# main entry point
def main():
    global serversock  # interpreter needs a hint here
      
    serversock = _listen(port)
    read_socks[serversock] = 1
    loop()

# socket listening loop
def loop():
    while 1:
        try:
            read, write, error = select.select(read_socks.keys(), [], [], 60)
            break
        
        # this happens if a client disconnects uncleanly
        except socket.error, e:
            if e.args[0] == EBADF:
                # just select everything until one errors
                for sock in read_socks:
                    try:
                        select.select([sock], [], [], 0)
                    except:
                        _logOut(sock)
                        read_socks.pop(sock)
                        break
    try:                
        for sock in read:
            # on the listening server socket, accept new connections
            if sock.fileno() == serversock.fileno():
                client, address = sock.accept()
                client.setblocking(False)
                
                chatClient = ChatClient(client)
                read_socks[client] = chatClient
                #write_socks[client] = 1#chatClient
                
            # handle regular input
            else:
                data = sock.recv(1024)
                if data:
                    if not ValidateCommand(data):
                        ERR(sock)
                    else:
                        read_socks[sock].execute(data)
                else:
                    _logOut(sock)
                    read_socks.pop(sock)
                    sock.close()
    
    # if the select() above fails, read/write/error will be invalid names, and the for
    # loop will throw an error.  ignore it and keep looping.                
    except NameError:
        pass
    
    loop()


if __name__ == "__main__": main()