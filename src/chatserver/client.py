from server import Server
from command import COMMANDS
from command import ParseCommand
from zope.interface import Interface, implements

def SEND(sobj, msg):
    sobj.send(msg.strip() + r"\r\n")

def ACK(sobj):
    SEND(sobj, "OK")
    
def ERR(sobj):
    SEND(sobj, "ERROR")    


class IChatClient(Interface):
    """This interface forces implementing classes to have a method available to 
    handle each command a client can send"""
    pass

for cmd in COMMANDS:
    setattr(IChatClient, cmd.upper(), lambda: False)


class Client():
    """This is a dumb pass-through client.  The complexity is on the server side"""
    implements(IChatClient)
    __sobj = None
    
    # this nickname tracking is a speedup, so that bogus commands don't get sent to the
    # server side and cost a lot of processing power in terms of dict lookups
    __nickname = None
    
    def __init__(self, socketObj):
        self.__sobj = socketObj
    
    def execute(self, cmd):
        command, parameters = ParseCommand(cmd)
        getattr(self, command)(parameters.split(" "))
    
    def getNickname(self):
        return self.__nickname
    
    
    def LOGIN(self, args):
        nickname = args[0]
        
        # users can't change nicks, and once logged in can't log in again
        if self.__nickname is not None:
            ERR(self.__sobj)
            
        try:
            Server.login(nickname, self)
            self.__nickname = nickname
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)
    
    
    def LOGOUT(self, args):
        
        # users can't log out before they're logged in
        if self.__nickname is None:
            ERR(self.__sobj)
            
        try:
            Server.logout(self.__nickname, self)
            self.__nickname = None
            ACK(self.__sobj)
        except:
            ERR(self.__sobj) 
        
        self.__sobj.close()      
    
    
    def JOIN(self, args):
        channel = args[0]
        
        # can't join a channel if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
        
        try:
            Server.join(self.__nickname, channel, self)
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)

    
    def PART(self, args):
        channel = args[0]
        
        # can't part a channel if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
        
        try:
            Server.part(self.__nickname, channel, self)
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)
        
    
    
    def MSG(self, args):
        target = args[0]
        message = " ".join(args[1:])
        
        # can't send a message if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
        
        try:
            Server.msg(self.__nickname, target, message, self)
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)
    

    # the two following callback methods should only be called from the server
    def GOTROOMMSG(self, args):
        SEND(self.__sobj, "GOTROOMMSG " + " ".join(args))
    
    def GOTUSERMSG(self, args):
        SEND(self.__sobj, "GOTUSERMSG " + " ".join(args))
        
