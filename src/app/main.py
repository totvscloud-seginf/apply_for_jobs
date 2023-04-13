from flask import Flask
from src.app.controller.generate_url_controller import GenerateUrlController
from src.app.controller.show_password_controller import ShowPasswordController
from cryptography.fernet import Fernet

app = Flask(__name__)

# TODO utilizar AWS para armazenar a chave secreta e parar de gerar aleatória
secret_key = Fernet.generate_key()

@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response

@app.route('/generate_url', methods=['POST'])
def generate_url():
    return GenerateUrlController(secret_key).generate_url()

@app.route('/password/', methods=['POST'])
def show_password():
    return ShowPasswordController(secret_key).show_password()

if __name__ == '__main__':
    app.run()
