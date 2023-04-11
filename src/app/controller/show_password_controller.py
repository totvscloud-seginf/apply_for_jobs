from datetime import datetime
from flask import request

from src.app.database.database import Database


class ShowPasswordController:
    def __init__(self):
        self.db = Database().collection

    def show_password(self, password_uuid):
        password_data = self.db.find_one({'uuid': str(password_uuid)})
        password_id = password_data['_id']
        if not password_data:
            return 'URL inválida'
        if password_data['views_left'] == 0:
            self.db.delete_one({'_id': password_id})
            return 'Visualizações esgotadas'
        if password_data['expires_at'] < datetime.utcnow():
            self.db.delete_one({'_id': password_id})
            return 'URL expirada'
        password = password_data['password']
        self.db.update_one({'_id': password_id}, {'$inc': {'views_left': -1}})
        return 'Sua senha é: ' + password
