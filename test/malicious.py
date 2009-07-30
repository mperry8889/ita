#!/usr/bin/python

import unittest
import socket

from common import connect, disconnect, sendCmd

sock = connect()
while 1:
    sock.send("x")

