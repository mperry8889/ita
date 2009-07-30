#!/usr/bin/python

# this in particular would be a lot easier and more robust with twisted

from common import connect, disconnect, sendCmd
from threading import Thread, Semaphore
import re
import time

def SendIter(sock, i):
    sendCmd(sock, "MSG #foo %d" % i)

def ReadIter(sock, i):
    data = sock.recv(1024)
    print data
    m = re.match("GOTROOMMSG (\w+) #iter (\d+)", data)
    if int(m.group(1)) != i:
        print "Error!"


sockOne = connect()
sendCmd(sockOne, "LOGIN sockOne")
sendCmd(sockOne, "JOIN #iter")
sockTwo = connect()
sendCmd(sockTwo, "LOGIN sockTwo")
sendCmd(sockTwo, "JOIN #iter")

for i in range(0, 10):
    SendIter(sockOne, i)
    ReadIter(sockTwo, i)

import sys
sys.exit()

# two clients, increment a number
sem = Semaphore()

def ThreadOne():
    regex = re.compile("GOTROOMMSG two #i (\d+)")
    sock = connect()
    sendCmd(sock, "LOGIN one\r\n")
    sendCmd(sock, "JOIN #i\r\n")
    
    while 1:
        data = sock.recv(4096)
        m = regex.match(data)
        if m is not None:
            str = m.group(1)
            print "1 str=%s" % str
            integer = int(str) + 1
            print "1 data = " + sendCmd(sock, "MSG #i %d\r\n" % integer)
            if integer > 4:
                sem.release()
                break
        else:
            print "1 no regex match! data is %s" % data
            break
            

def ThreadTwo():
    regex = re.compile("GOTROOMMSG one #i (\d+)")
    sock = connect()
    sendCmd(sock, "LOGIN two\r\n")
    sendCmd(sock, "JOIN #i\r\n")
    sendCmd(sock, "MSG #i 1\r\n")
              
    while 1:
        data = sock.recv(4096)
        m = regex.match(data)
        if m is not None:
            str = m.group(1)
            print "2 str=%s" % str
            integer = int(str) + 1
            print "2 data = " + sendCmd(sock, "MSG #i %d\r\n" % integer)
            if integer > 4:
                break
                sem.release()
        else:
            print "2 no regex match! data is %s" % data
            break

Thread(target=ThreadOne).start()
time.sleep(0.5)
Thread(target=ThreadTwo).start()
sem.acquire(True)

print "OK!"

