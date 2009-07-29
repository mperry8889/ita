import logging as log

log.basicConfig(level=log.DEBUG)

class _Server():
    __users = {}
    __channels = {}
    
    def __init__(self):
        pass
    
    def login(self, nick, obj):
        if nick in self.__users.keys():
            raise Exception
        
        self.__users[nick] = obj
        log.debug("Login: %s" % nick)
    
    
    def logout(self, nick, obj):
        if nick is None: return
        if nick not in self.__users.keys():
            raise Exception
        
        self.__users.pop(nick)
        log.debug("Logout: %s" % nick)
    
    def join(self, nick, channel, obj):
        if self.__channels.has_key(channel):
            self.__channels[channel].append(nick)
        else:
            self.__channels[channel] = [nick]
        log.debug("%s: %s has joined" % (channel, nick))
    
    def part(self, nick, channel, obj):
        if not self.__channels.has_key(channel):
            raise Exception
        if nick not in self.__channels[channel]:
            raise Exception
        
        self.__channels[channel].pop(nick)
        log.debug("%s: %s has parted" % (channel, nick))
        

    def msg(self, nick, target, message, obj):
        if '#' in target:
            self.__msg_channel(nick, target, message, obj)
        else:
            self.__msg_user(nick, target, message, obj)
    
    def __msg_channel(self, nick, channel, message, obj):
        if not self.__channels.has_key(channel):
            raise Exception
        if nick not in self.__channels[channel]:
            raise Exception
        
        for user in self.__channels[channel]:
            self.__users[user].GOTROOMMSG([nick, channel, message])
        log.debug("%s: <%s> %s" % (channel, nick, message))
        
          
    def __msg_user(self, nick, target, message, obj):
        if nick not in self.__users.keys():
            raise Exception
        
        self.__users[target].GOTUSERMSG([nick, message])
        log.debug("%s -> %s: %s" % (nick, target, message))
        

Server = _Server()