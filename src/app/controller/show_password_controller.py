from datetime import datetime
from flask import request
from src.app.database.database import Database
from cryptography.fernet import Fernet


class ShowPasswordController:
    def __init__(self, secret_key):
        self.db = Database("passwords")
        self.fernet = Fernet(secret_key)

    def show_password(self):
        password_uuid = request.json.get('password_uuid')
        code = request.json.get('code')
        password_data = self.db.find_one(str(password_uuid), code)
        if not password_data:
            return 'URL inválida'
        if password_data['views_left'] == 0:
            self.db.delete_one(str(password_uuid), code)
            return 'Visualizações esgotadas'
        if datetime.strptime(password_data['expires_at'], '%Y-%m-%d %H:%M:%S.%f') < datetime.utcnow():
            self.db.delete_one(str(password_uuid), code)
            return 'Link expirado !'
        encrypted_password = password_data['password']
        password = self.fernet.decrypt(bytes(encrypted_password)).decode('utf-8')
        self.db.update_one(str(password_uuid), code, 'SET views_left = views_left - :val')
        return password
