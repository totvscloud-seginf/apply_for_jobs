from uuid import uuid4

from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

# Database connection
client = MongoClient('mongodb://localhost:27017/')
db = client['totvs_password']
collection = db['passwords']


# Generate URL
@app.route('/generate_url', methods=['POST'])
def generate_url():
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

    collection.insert_one(password_data)

    return request.host_url + 'password/' + str(password_uuid)


# Show URL
@app.route('/password/<password_uuid>')
def show_password(password_uuid):
    password_data = collection.find_one({'uuid': str(password_uuid)})
    password_id = password_data['_id']
    if not password_data:
        return 'URL inválida'
    if password_data['views_left'] == 0:
        collection.delete_one({'_id': password_id})
        return 'Visualizações esgotadas'
    if password_data['expires_at'] < datetime.utcnow():
        db.passwords.delete_one({'_id': password_id})
        return 'URL expirada'
    password = password_data['password']
    collection.update_one({'_id': password_id}, {'$inc': {'views_left': -1}})
    return 'Sua senha é: ' + password


if __name__ == '__main__':
    app.run()
