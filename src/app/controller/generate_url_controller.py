from uuid import uuid4
from datetime import datetime, timedelta
from flask import request

from src.app.database.database import Database


class GenerateUrlController:
    def __init__(self):
        self.db = Database().collection

    def generate_url(self):
        password = request.form['password']
        views = int(request.form['views'])
        validity = int(request.form['validity'])
        expires_at = datetime.utcnow() + timedelta(hours=validity)

        password_uuid = str(uuid4())

        password_data = {
            'uuid': password_uuid,
            'password': password,
            'views_left': views,
            'expires_at': expires_at
        }

        self.db.insert_one(password_data)

        return request.host_url + 'password/' + str(password_uuid)
