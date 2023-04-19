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
        userDATA['password']['auto'] = 'false'
        _pass = passGen(userDATA['password']) 
        self.password = _pass.getpass()
        conector = Database()
        
        epoch_now = int(datetime.now().timestamp())
        
        query = conector.user_login(self.user_login,  self.password)
        
        for login_info in query:
            if 'result' in login_info:
                return login_info
            if login_info['passlifetime'] < epoch_now:
                return {'result': 'FAIL', 'err_code': 7440, 'data': 'Sua senha expirou, gere uma nova senha'}
            if login_info['passtatus'] == 0:
                return {'result': 'FAIL', 'err_code': 7340, 'data': 'Sua senha não é mais válida'}
            
        return {'result': 'OK', 'err_code': 0, 'data': 'Logado com sucesso'}
         
 
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
        epoch_now = int(datetime.now().timestamp())

        if password['passlimitview'] == 0:
            conector.update_password_status(password['userid'], password['passid'])
            return {'result': 'WARNING', 'err_code': '440', 'data': 'O link não é mais válido'}
                
        if epoch_now > password['passlifetime']:
            conector.update_password_status(password['userid'], password['passid'])
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O link não é mais válido'}
        
        limitview = password['passlimitview']
        
        if limitview == 0:
            conector.update_password_status(password['userid'], password['passid'])
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O limite de visualização foi atingido'}
        
        return conector.update_userpass_limitview(password['userid'], password['passid'], limitview-1)
               
    def do_user_add_newpass(self, userDATA):
        conector = Database()
        self.user_login = userDATA['login']
       
        self.password = passGen(userDATA['password']) 
        userDATA['password']['password'] = self.password.getpass()

        return conector.add_new_pass(self.user_login, userDATA['password'])

    def do_user_get_link(self, userDATA):
        #Busca o link para acesso
        conector = Database()
        self.user_login = userDATA['login']
        
        query = conector.user_query(self.user_login)
        
        #atualizando informacao do passwordview
        
        for pass_list in query:
            if pass_list['passtatus'] != 0:
                return pass_list         
        
        return {'result': 'WARNING', 'err_code': '7330', 'data': 'Não há links válidos, gere um novo passowrd'}
        
        
    def do_user_use_link(self, userDATA):
        #Busca o link para acesso
        conector = Database()
        self.user_login = userDATA['login']
        
        url = userDATA['password']['url']
        #cruar um novo metodo exclusivo para consulta do link
        query = conector.user_query(self.user_login)
        response = {}
        for pass_list in query:
            if 'currentlink' in pass_list:
                if pass_list['currentlink'] == url and pass_list['passtatus'] != 0:
                    viewCheck = self.do_user_password_view(pass_list)
                    if 'result' in pass_list:
                        if viewCheck['result'] != 'OK' :
                            response = viewCheck
                        else:
                            response = pass_list
                    else:
                        response = pass_list
                else:
                    conector.update_password_status(pass_list['userid'], pass_list['passid'])
                    return {'result': 'WARNING', 'err_code': '330', 'data': 'O link não é mais válido'}
            else:
                response = pass_list
        #atualizando informacao do passwordview
        
        return response 