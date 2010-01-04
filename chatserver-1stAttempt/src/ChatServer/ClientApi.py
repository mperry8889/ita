class ClientApi(object):

   def __init__(self):
      raise NotImplementedError

   def Login(self, handle):
      raise NotImplementedError

   def Logout(self):
      raise NotImplementedError

   def SendMsg(self, msg):
      raise NotImplementedError

   def RecvMsg(self, msg):
      raise NotImplementedError


