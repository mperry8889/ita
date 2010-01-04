#!/usr/bin/python

from common import connect, disconnect, sendCmd
from threading import Thread

def NormalOp(i):
    print "Go! %d"%i
    sock = connect()
    sendCmd(sock, "LOGIN foo%d\r\n" % i)
    sendCmd(sock, "JOIN #foo\r\n")
    sendCmd(sock, "MSG #foo hello\r\n")
    sendCmd(sock, "MSG foo%d sup\r\n" % i)
    sendCmd(sock, "PART #foo\r\n")
    sendCmd(sock, "LOGOUT\r\n")
    disconnect(sock)
    

# normal operation
for i in range(0, 10000):
    NormalOp(i)
    
# quit by just closing the connection
for i in range(0, 10000):
    sock = connect()
    sendCmd(sock, "LOGIN foo%d\r\n" % i)
    sendCmd(sock, "JOIN #foo\r\n")
    sendCmd(sock, "MSG #foo hello\r\n")
    sendCmd(sock, "MSG foo%d sup\r\n" % i)
    disconnect(sock)

# 50 threads all connecting and operating normally
for j in range(0, 10000):
    for i in range(0, 50):
        Thread(target=NormalOp, args=(i,)).start()