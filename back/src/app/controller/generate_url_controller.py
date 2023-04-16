import json
import random
import string
from uuid import uuid4
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from back.src.app.database.database import Database


def has_missing_attributes(event):
    required_attributes = ['passwordOptions', 'views', 'validity', 'code']
    for attr in required_attributes:
        if attr not in event or not event[attr]:
            return True
    return False


class GenerateUrlController:
    def __init__(self, public_key):
        self.public_key = public_key
        self.db = Database("passwords")

    def generate_url(self, event):

        if has_missing_attributes(event):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "missing attributes"})
            }

        password_options = event['passwordOptions']
        password = ''

        # Se enviou senha customizada ou nao
        if password_options == "custom":
            if 'password' not in event or not event['password']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': "missing attributes"})
                }
            password = event['password']
        else:
            characters = ''
            password_length = 8
            if password_options == "simple":
                characters = string.ascii_letters + string.digits
            elif password_options == "medium":
                characters = string.ascii_letters + string.digits
                password_length = 12
            elif password_options == "strong":
                characters = string.ascii_letters + string.digits + string.punctuation
                password_length = 16
            password = ''.join(random.choice(characters) for i in range(password_length))

        views = event['views']
        validity = event['validity']
        code = event['code']
        expires_at = datetime.utcnow() + timedelta(hours=validity)

        password_uuid = str(uuid4())
        encrypted_password = \
            self.public_key.encrypt(bytes(password.encode('utf-8')),
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                 algorithm=hashes.SHA256(), label=None))

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
