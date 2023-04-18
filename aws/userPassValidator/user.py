import json
from conn import Database
import base64
from datetime import datetime
from passGenerator import passGen

class user:
    def __init__(self):
        self.user_login = None
        self.password = None
        
    def do_user_link_gen(self):
        """Gera o hash do link"""
        date_now = datetime.now()
        date_now = date_now.strftime("%d/%m/%Y %H:%M:%S")
        encode_time = base64.b64encode(date_now.encode("utf-8"))
        encoded_login = base64.b64encode(self.user_login.encode("utf-8"))
        userencrypt = {'datetime':  str(encode_time, "utf-8"), 'user':  str(encoded_login, "utf-8")}
       
        return userencrypt
    
    def do_user_login(self, userDATA):
        """Realizar login"""
        self.user_login = userDATA['login']
        conector = Database()
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

        self.user_login = newUSERDATA['login']

        conector = Database() 
        #novo usuario nunca tera link, mas vou deixar isso por enquanto 
        if len(newUSERDATA['password']['currentlink']) == 0:
            new_link = self.do_user_link_gen()
            acces_link = f"use_key={new_link['user']}&user_x={new_link['datetime']}"
            newUSERDATA['password']['currentlink'] = acces_link
        
        ##protegendo a senha
        passwrd = newUSERDATA['password']
        new_pass = passGen(passwrd)
        
        newUSERDATA['password']['password'] = new_pass.getpass()
        
        #return newUSERDATA['password']
        
        saveuser = conector.put_user(self.user_login, newUSERDATA['password'])
        
        return saveuser
        
    def do_user_password_view(self, password):
        """Aqui define se o usuário pode ou não logar com o link de acesso"""
        conector = Database()
        epoch_now = int(datetime.datetime.now().timestamp())

        if epoch_now > password['passlifetime']:
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O link não é mais válido'}
        
        limitview = password['passlimitview']
        if limitview == 0:                
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O limite de visualização foi atingido'}
        
        return conector.update_userpass_limitview( password['userid'], password['passid'], limitview-1)
               
    def do_user_add_newpass(self, newpass):
        conector = Database()
        userlogin = conector.user_query(self.user_login)
        if newpass['auto']:
            new_pass = passGen(newpass)
            self.password['password'] = new_pass            
        else:
            self.password['password'] = new_pass

        conector.add_new_pass(userlogin['userid'], self.password)
     
    def do_user_get_link(self, userDATA):
        #Busca o link para acesso
        conector = Database()
        self.user_login = userDATA['login']
        
        #cruar um novo metodo exclusivo para consulta do link
        response = conector.user_query(self.user_login)
        #atualizando informacao do passwordview
        
        viewCheck = self.do_user_password_view(response)

        if viewCheck['result'] != 'OK' :
            response = viewCheck

        return response