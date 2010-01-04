#!/usr/bin/env python

from ChatServer import Dispatcher
from optparse import OptionParser
import logging

# command line arguments
optp = OptionParser()
optp.add_option("-p", "--port",
                help = "port",
                dest = "port",
                default = 6667)
optp.add_option("-v", "--verbose",
                help = "verbose server",
                dest = "verbose",
                action = "store_true")
(args, argv) = optp.parse_args()

# initialize logging
logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO)

# fire up the server
d = Dispatcher(port = args.port)