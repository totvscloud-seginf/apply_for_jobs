from uuid import uuid4
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from flask import request
from src.app.database.database import Database


class GenerateUrlController:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.db = Database("passwords")
        self.fernet = Fernet(self.secret_key)

    def generate_url(self):
        password = request.form['password']
        views = int(request.form['views'])
        validity = int(request.form['validity'])
        code = int(request.form['code'])
        expires_at = datetime.utcnow() + timedelta(hours=validity)

        password_uuid = str(uuid4())
        encrypted_password = self.fernet.encrypt(bytes(password.encode('utf-8')))

        password_data = {
            'id': password_uuid,
            'password': encrypted_password,
            'views_left': views,
            'expires_at': str(expires_at),
            'code': code,
        }

        self.db.insert_one(password_data)

        return str(password_uuid)
