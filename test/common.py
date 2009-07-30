import socket

server = "127.0.0.1"
port = 6668

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    return sock
    
def disconnect(sock):
    sock.close()

def sendCmd(sock, cmd):
    sock.send(cmd)