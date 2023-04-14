import json
import conn
import base64
from datatime import datatime, timedelta
from re import search

class user:
    def __init__(self, userAUTH):
        self.user_login = userAUTH.login
        self.password = userAUTH.password
        
    def doUserLogin(self):
        return
      
        
    def doUserLink(self):
        userlogin = self.user_login
        encoded_bytes = base64.b64encode(userlogin.encode("utf-8"))
        userencrypt = str(encoded_bytes, "utf-8")
       
        return userencrypt
        
    def doUserPasswordView(self):
        
        return
        
    def doUserPassUpdate(self, userDATA):
        self.user_login = userDATA.login
        self.password = userDATA.password
        
    