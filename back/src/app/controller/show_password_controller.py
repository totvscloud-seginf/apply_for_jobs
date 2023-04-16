import json
from datetime import datetime
from back.src.app.database.database import Database
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class ShowPasswordController:
    def __init__(self, private_key):
        self.db = Database("passwords")
        self.private_key = private_key

    def show_password(self, event):
        if 'password_uuid' not in event or not event['password_uuid'] or 'code' not in event or not event['code']:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "missing attributes"})
            }

        password_uuid = event['password_uuid']
        code = event['code']
        password_data = self.db.find_one(str(password_uuid), code)
        if not password_data:
            return {'statusCode': 400, 'message': 'Invalid URL'}
        if password_data['views_left'] == 0:
            self.db.delete_one(str(password_uuid), code)
            return {'statusCode': 400, 'message': 'Views exhausted'}
        if datetime.fromisoformat(password_data['expires_at']) < datetime.now():
            self.db.delete_one(str(password_uuid), code)
            return {'statusCode': 400, 'message': 'Link expired!'}
        encrypted_password = password_data['password']
        password = self.private_key.decrypt(encrypted_password,
                                            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                         algorithm=hashes.SHA256(), label=None)
                                            ).decode('utf-8')
        self.db.update_one(str(password_uuid), code, 'SET views_left = views_left - :val')
        return {
            'statusCode': 200,
            'body': json.dumps({'password': password})
        }
