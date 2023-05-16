import random
import string
import uuid
import time
from app.models.PasswordModel import RequestPassword
from app.service.SavePassword import SavePassword

class PasswordGenerator:
    def __init__(self):
        pass

    def generate_password(self, length, use_words=True, use_numbers=True, use_symbols=True):

        chars = ""
        if use_words:
            chars += string.ascii_letters
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += "{!#$%&(*+@^-)"

        password = "".join(random.choice(chars) for _ in range(length))
        return password
    
    def generate_password_data(self, request_password:RequestPassword):
        
        if request_password.password == "":
            password = self.generate_password(request_password.length, request_password.use_words, request_password.use_numbers, request_password.use_symbols)
        else:
            password = request_password.password

        valid_until = time.time() + request_password.valid_days * 24 * 3600

        password_data = {
            'email': request_password.email,
            'password': password,
            "max_views": request_password.max_views,
            "valid_until": valid_until,
            "num_views": 0,
        }

        save = SavePassword()
        saved = save.save_password(password_data=password_data)

        if saved:
            return True
        else:
            return False

  