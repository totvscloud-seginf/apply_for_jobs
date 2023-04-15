import json
from uuid import uuid4
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from back.src.app.database.database import Database


class GenerateUrlController:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.db = Database("passwords")
        self.fernet = Fernet(self.secret_key)

    def generate_url(self, event):
        if 'password' not in event or 'views' not in event or 'validity' not in event or 'code' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "missing attributes"})
            }

        password = event['password']
        views = event['views']
        validity = event['validity']
        code = event['code']
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

        return {
            'statusCode': 200,
            'body': json.dumps({'password_id': password_uuid})
        }
