from flask import Flask
from src.app.controller.generate_url_controller import GenerateUrlController
from src.app.controller.show_password_controller import ShowPasswordController

app = Flask(__name__)

@app.route('/generate_url', methods=['POST'])
def generate_url():
    return GenerateUrlController().generate_url()

@app.route('/password/<password_uuid>')
def show_password(password_uuid):
    return ShowPasswordController().show_password(password_uuid)

if __name__ == '__main__':
    app.run()
