from server import Server
from common import ACK, ERR, SEND
from command import COMMANDS
from command import ParseCommand
from zope.interface import Interface, implements


# this interface creates a stub method for each command in command.py, and 
# enforces that the client below implements each method correctly.  this is largely
# useless for this project since the parameters won't ever change, but in the odd event
# a command is added, this interface will enforce that a handler is added in client code
#class IChatClient(Interface):
#    pass

#for cmd in COMMANDS:
#    setattr(IChatClient, cmd.upper(), lambda: False)


# dumb pass-through client, which just sends commands over to the server
class Client():
#    implements(IChatClient)
    __sobj = None
    
    # this nickname tracking is a speedup, so that bogus commands don't get sent to the
    # server side and cost a lot of processing power in terms of dict lookups
    __nickname = None
    
    def __init__(self, socketObj):
        self.__sobj = socketObj
    
    # execute a command sent from the client
    def execute(self, cmd):
        command, parameters = ParseCommand(cmd)
        getattr(self, command)(parameters.split(" "))
    
    def getSocketObj(self):
        return self.__sobj
    
    def getNickname(self):
        return self.__nickname
    
    ##
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
    
    ##
    def LOGOUT(self, args):
        
        # users can't log out before they're logged in
        if self.__nickname is None:
            ERR(self.__sobj)
            return
            
        try:
            Server.logout(self.__nickname, self)
            self.__nickname = None
            ACK(self.__sobj)
        except:
            ERR(self.__sobj) 
        
        self.__sobj.close()  
    
    ##
    def JOIN(self, args):
        channel = args[0]
        
        # can't join a channel if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
            return
        
        try:
            Server.join(self.__nickname, channel, self)
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)

    ##
    def PART(self, args):
        channel = args[0]
        
        # can't part a channel if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
            return
        
        try:
            Server.part(self.__nickname, channel, self)
            ACK(self.__sobj)
        except:
            ERR(self.__sobj)
        
    ##    
    def MSG(self, args):
        target = args[0]
        message = " ".join(args[1:])
        
        # can't send a message if not logged in
        if self.__nickname is None:
            ERR(self.__sobj)
            return
        
        # we won't ACK this on this side - the server has to do it,
        # before it fires the callback.  kinda of lame and sphagetti like
        try:
            Server.msg(self.__nickname, target, message, self)
        except:
            ERR(self.__sobj)
    

    # the two following callback methods should only be called from the server
    def GOTROOMMSG(self, args):
        SEND(self.__sobj, "GOTROOMMSG " + " ".join(args))
    
    def GOTUSERMSG(self, args):
        SEND(self.__sobj, "GOTUSERMSG " + " ".join(args))
        
