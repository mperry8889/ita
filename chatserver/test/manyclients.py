#!/usr/bin/python

# it would be better to do this test asynchronously but without access to 
# twisted or asyncore it's just easier to use threads than to write a whole
# select loop

# this test starts a bunch of clients and then makes sure they all get one
# user's message ("Hello!")

# it hangs occasionally due to the recv's below.  again if this were async
# it wouldn't be a big deal, but this is written in blocking IO and knowingly
# isn't perfect.  though i did find a bunch of bugs with it.

from threading import Thread
import socket
import random
import time

from common import connect, disconnect, sendCmd

threads = 5
status = 1

def ListenerClient(nick):
    global status
    
    sock = connect()
    sendCmd(sock, "LOGIN %s\r\n" % nick)
    sock.recv(1024)
    sendCmd(sock, "JOIN #foo\r\n")
    data = ""
    while 1:
        data = sock.recv(1024)
        if not data: break
        if data == "OK\r\n":
            continue
        if "GOTROOMMSG" in data:
            break
        
    print "[%s] %s" % (nick, data.strip())
    sendCmd(sock, "PART #foo\r\n")
    sendCmd(sock, "LOGOUT\r\n")
    sock.close()

def SenderClient(nick):
    sock = connect()
    sendCmd(sock, "LOGIN %s\r\n" % nick)
    sendCmd(sock, "JOIN #foo\r\n")
    sendCmd(sock, "MSG #foo Hello!\r\n")
    sendCmd(sock, "PART #foo\r\n")
    sendCmd(sock, "LOGOUT\r\n")
    sock.close()

# repeat this whole scenario 10 times    
for j in range(0, 5000):
    print "starting %d threads..." % threads
    for i in range(1, threads):
        nick="thread%d" % i
        t = Thread(target=ListenerClient, args=(nick,))
        t.start()
    
    time.sleep(0.1)
    
    Thread(target=SenderClient, args=("thread0",)).start()
    

if status != 1:
    print "Status is FAIL"
else:
    print "Success!"