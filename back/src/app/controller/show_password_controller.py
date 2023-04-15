import json
from datetime import datetime
from back.src.app.database.database import Database
from cryptography.fernet import Fernet


class ShowPasswordController:
    def __init__(self, secret_key):
        self.db = Database("passwords")
        self.fernet = Fernet(secret_key)

    def show_password(self, event):
        if 'password_uuid' not in event or 'code' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "missing attributes"})
            }

        password_uuid = event['password_uuid']
        code = event['code']
        password_data = self.db.find_one(str(password_uuid), code)
        if not password_data:
            return {'message': 'Invalid URL'}
        if password_data['views_left'] == 0:
            self.db.delete_one(str(password_uuid), code)
            return {'message': 'Views exhausted'}
        if datetime.fromisoformat(password_data['expires_at']) < datetime.now():
            self.db.delete_one(str(password_uuid), code)
            return {'message': 'Link expired!'}
        encrypted_password = password_data['password']
        password = self.fernet.decrypt(bytes(encrypted_password)).decode('utf-8')
        self.db.update_one(str(password_uuid), code, 'SET views_left = views_left - :val')
        return {
            'statusCode': 200,
            'body': json.dumps({'password': password})
        }
