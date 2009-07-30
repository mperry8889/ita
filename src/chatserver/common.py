def SEND(sobj, msg):
    sobj.send(msg.strip() + "\r\n")

def ACK(sobj):
    SEND(sobj, "OK")
    
def ERR(sobj):
    SEND(sobj, "ERROR")

def ERRMSG(sobj, msg):
    SEND(sobj, "ERROR %s" % msg)  