import json
import conn
import base64
import datetime
from re import search

class user:
    def __init__(self, userAUTH):
        self.user_login = userAUTH.login
        self.password = userAUTH.password
    
    def do_user_login(self, link=None):
        """Realizar login"""
        conector = conn()

        if link:
            link = self.do_user_link_gen()
        
        userlogin = conector.user_query(self.user_login)
        return userlogin
     
    def do_save_new_user(self, newUSERDATA):
        """Salva novo usuário"""
        conector = conn()  
        return  conector.put_item(self.user_login, self.password)
        
    def do_user_link_gen(self):
        """Gera o hash do link"""
        epoch_now = int(datetime.datetime.now().timestamp())
        encode_time = base64.b64encode(epoch_now.encode("utf-8"))
        userlogin = self.user_login
        encoded_login = base64.b64encode(userlogin.encode("utf-8"))
        userencrypt = {'datetime':  str(encode_time, "utf-8"), 'user':  str(encoded_login, "utf-8")}
       
        return userencrypt
        
    def do_user_password_view(self, link):
        """Aqui define se o usuário pode ou não logar com o link de acesso"""
        conector = conn()  
        passcountview = conector.user_query(self.user_login)
        epoch_now = int(datetime.datetime.now().timestamp())
        if epoch_now > passcountview.passlifetime:
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O link não é mais válido'}
        
        if link != passcountview.currentlink:
              return {'result': 'WARNING', 'err_code': '0', 'data': 'O link não é mais válido'}
        
        limitview = int(passcountview.passlimitview)

        if limitview == 0:                
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O limite de visualização foi atingido'}
        
        conector.update_userpass_limitview(passcountview.userid, passcountview.passid, limitview-1)
        
    def do_user_add_newpass(self):
        conector = conn() 
        userlogin = conector.user_query(self.user_login)
        conector.add_new_pass(userlogin.userid, )

        
    