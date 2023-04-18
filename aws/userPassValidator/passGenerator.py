import base64
import json
import random
import string

class passGen:
    #colocar descricao 
    def __init__(self, PARAMETERS):
        self._pass = PARAMETERS['password']
        #params espera receber uma lista dos parametros definidos
        #assim caso surga um novo parametro sua implementação fica mais simples.
        self.params = PARAMETERS['params']
        self.autopass = PARAMETERS['auto']
        self.passLen   = self.params['passlen']
        
    def passGen(self):
        #colocar descricao
        newpass = []
        for i in range(self.passlen):
            for parameters in self.params:
                if parameters == 'numbers':
                    newpass.append(random.choice(string.digits))
                if parameters == 'letter':
                    newpass.append(random.choice(string.ascii_letters))
                if parameters == 'espChar':
                    newpass.append(random.choice(string.punctuation))
        
        return ''.join(newpass)
    
    #verificar se criar um método no request para realizar encriptação é melhor, para isso ver substituição de valor do objeto
    def passProtect(self, password):
        encoded_bytes = base64.b64encode(password.encode("utf-8"))
        passprotected = str(encoded_bytes, "utf-8")
        
        return passprotected
    
    def getpass(self):
        
        if self.autopass == 'false':
            return self.passProtect(self._pass)    
        
        return self.passProtect(self.passGen())