#!/usr/bin/python

# it would be better to do this test asynchronously but without access to 
# twisted or asyncore it's just easier to use threads than to write a whole
# select loop

# this test starts a bunch of clients and then makes sure they all get one
# user's message ("Hello!")

from threading import Thread
import socket
import random
import time

from common import connect, disconnect, sendCmd

threads = 10
status = 1

def ListenerClient(nick):
    global status
    
    sock = connect()
    sendCmd(sock, "LOGIN %s\r\n" % nick)
    sock.recv(1024)
    sendCmd(sock, "JOIN #foo\r\n")
    sock.recv(1024)
    
    data = sock.recv(1024)
    if "GOTROOMMSG thread0 #foo Hello!\r\n" not in data:
        print "%s got a different message: %s" % (nick, data)
        status = 0
        return
    print "[%s] %s" % (nick, data.strip())
    sendCmd(sock, "LOGOUT\r\n")
    sock.close()

def SenderClient(nick):
    sock = connect()
    sendCmd(sock, "LOGIN %s\r\n" % nick)
    sendCmd(sock, "JOIN #foo\r\n")
    sendCmd(sock, "MSG #foo Hello!\r\n")
    sendCmd(sock, "LOGOUT\r\n")
    sock.close()

# repeat this whole scenario 10 times    
for j in range(0, 1):
    print "starting %d threads..." % threads
    for i in range(1, threads):
        nick="thread%d" % i
        t = Thread(target=ListenerClient, args=(nick,))
        t.start()
    
    time.sleep(0.25)
    
    Thread(target=SenderClient, args=("thread0",)).start()
    

if status != 1:
    print "Status is FAIL"
else:
    print "Success!"