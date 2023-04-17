import json
import conn
import base64
import datetime
import passGenerator

class user:
    def __init__(self, userAUTH):
        self.user_login = userAUTH.login
        self.password = userAUTH.password
    
    def do_user_login(self):
        """Realizar login"""
        conector = conn()
        userlogin = conector.user_query(self.user_login)
        if userlogin['result']:
            return userlogin

        if userlogin['password'] == base64.b64encode(self.password.encode("utf-8")):
                return {'result': 'ERROR', 'err_code': 3000, 'data': "Password inválido"}

        epoch_now = int(datetime.datetime.now().timestamp())
        
        if userlogin['passlifetime'] < epoch_now:
            return {'result': 'ERROR', 'err_code': 4000, 'data': "Esse password expirou, é necessário gerar um novo"}
        
        return {'result': 'OK', 'err_code': 0, 'data': "Logado com sucesso"}
 
    def do_save_new_user(self, newUSERDATA):
        """Salva novo usuário"""
        conector = conn()  
        if newUSERDATA['link']:
            new_link = self.do_user_link_gen()
            newUSERDATA['currentlink'] = new_link

        if newUSERDATA['auto']:
            new_pass = passGenerator(self.password)
            self.password['password'] = new_pass
        
        saveuser = conector.put_item(self.user_login, self.password)
        
        return saveuser
        
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
        #Se tudo certo realiza login
        self.do_user_login()
        
    def do_user_add_newpass(self, newpass):
        conector = conn() 
        userlogin = conector.user_query(self.user_login)
        if newpass['auto']:
            new_pass = passGenerator(newpass)
            self.password['password'] = new_pass            
        else:
            self.password['password'] = new_pass

        conector.add_new_pass(userlogin.userid, self.password)

        
    