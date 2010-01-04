#!/usr/bin/python

import unittest
import socket
import sys

from common import connect, disconnect, sendCmd

print "infinite stream..."
try:
    pass
    sock = connect()
    while 1:
        sock.send("x")
    sock.close()
except:
    print "got exception!"
    print sys.exc_info()
    

print "login w/2KB username..."
try:
    sock = connect()
    cmd = "LOGIN "
    for i in range(1, 2048):
        cmd += "x"
    cmd += "\r\n"
    sendCmd(sock, cmd)
    data = sock.recv(1024)
    print "data = %s" % data   
    sendCmd(sock, "JOIN #foo")
    data = sock.recv(1024)
    print "data = %s" % data
    sock.close()
except:
    print "got exception!"
    print sys.exc_info()
    

print "normal read, just to see if the next select() is ok"
try:
    sock = connect()
    sendCmd(sock, "LOGIN foo\r\n")
    sendCmd(sock, "LOGOUT\r\n")
    sock.close()
except:
    print "something failed :("
    raise
else:
    print "worked fine"