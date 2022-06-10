from operator import truediv
import string
import random
import re
from datetime import datetime,timedelta

class Password:
    def __init__(self,tam) -> None:
        self.tam = tam
    
    def random_password(self) -> str:
        lower   = string.ascii_lowercase
        upper   = string.ascii_uppercase
        num     = string.digits
        symbols = '!#$%&*+->@_' #string.punctuation

        all_data = lower + upper + num + symbols
        temp = random.sample(all_data,self.tam)
        
        random_password = "".join(temp)

        return random_password

    def is_valid(self,random_password):
        has_lower   = re.findall('[a-z]',random_password)
        has_upper   = re.findall('[A-Z]',random_password)
        has_num     = re.findall('[0-9]',random_password)
        has_symbols = re.findall('[!-/:-?]',random_password)

        if has_lower and has_upper and has_num and has_symbols:
            return True
        else:
            return False

    def generate_password(self):
        if self.tam >= 8 and self.tam <= 50:
            while True:
                random_password = self.random_password()
                if self.is_valid(random_password):
                    return random_password
        else:
            return None
    
    @staticmethod
    def calculate_expiration_date(pDays: int):
        return (datetime.today() + timedelta(days=pDays))
