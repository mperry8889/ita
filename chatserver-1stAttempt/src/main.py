#!/usr/bin/env python

from ChatServer import ChatServer
from optparse import OptionParser
import socket
import logging


# command-line arguments
optp = OptionParser()
optp.add_option("-p", "--port",
                help = "port",
                dest = "port",
                default = 6667)
optp.add_option("-v", "--verbose",
                help = "verbose output",
                dest = "verbose",
                action = "store_true")

(args, argv) = optp.parse_args()


# initialize logging
logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO)


# fire up the server
cs = ChatServer.ChatServer(port = args.port)


