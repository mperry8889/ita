from common import ACK, ERR, SEND
import logging as log

log.basicConfig(level=log.INFO)

# an instance of this class is exposed, not the class itself.  this is so each
# client can access the same instance
class _Server():
    # these two dicts are the magic behind the chat server
    __users = {}
    __channels = {}
    
    # log in a user - add it to the __users dict
    def login(self, nick, obj):
        if nick is None:
            raise Exception
        if nick in self.__users.keys():
            raise Exception
        
        self.__users[nick] = obj
        log.debug("Login: %s" % nick)
    
    
    # log out a user - remove it from the __users dict
    def logout(self, nick, obj):
        if nick is None: return
        if nick not in self.__users.keys():
            raise Exception
        
        # part all channels as well. searching takes a while
        # so just iterate over the full list of channels, part the user,
        # and ignore any exceptions
        for channel in self.__channels.keys():
            try:
                self.part(nick, channel, obj)
            except:
                pass
        self.__users.pop(nick)
        log.debug("Logout: %s" % nick)
    
    
    # add a user to a channel.  add the user to the list associated
    # with the channel
    def join(self, nick, channel, obj):
        if self.__channels.has_key(channel):
            self.__channels[channel].append(nick)
        else:
            self.__channels[channel] = [nick]
        log.debug("%s: %s has joined" % (channel, nick))
    
    
    # remove a user from a channel's userlist
    def part(self, nick, channel, obj):
        if not self.__channels.has_key(channel):
            raise Exception
        if nick not in self.__channels[channel]:
            raise Exception
        
        self.__channels[channel].remove(nick)
        if self.__channels[channel] == []:
            self.__channels.pop(channel)
        log.debug("%s: %s has parted" % (channel, nick))
        

    # message handler
    def msg(self, nick, target, message, obj):
        if '#' in target:
            self.__msg_channel(nick, target, message, obj)
        else:
            self.__msg_user(nick, target, message, obj)
    

    # send a message to everyone in a channel
    def __msg_channel(self, nick, channel, message, obj):
        if not self.__channels.has_key(channel):
            raise Exception
        if nick not in self.__channels[channel]:
            raise Exception
        
        # we have to ACK here before the callback gets fired, so the user
        # knows the command was OK
        ACK(obj.getSocketObj())
        for user in self.__channels[channel]:
            self.__users[user].GOTROOMMSG([nick, channel, message])
        log.debug("%s: <%s> %s" % (channel, nick, message))
        

    # send a message to a single user          
    def __msg_user(self, nick, target, message, obj):
        if nick not in self.__users.keys():
            raise Exception
        
        ACK(obj.getSocketObj())
        self.__users[target].GOTUSERMSG([nick, message])
        log.debug("%s -> %s: %s" % (nick, target, message))


# create a _Server instance and expose it
Server = _Server()