import json
import os

from back.src.app.controller.generate_url_controller import GenerateUrlController
from back.src.app.controller.show_password_controller import ShowPasswordController

secret_key = os.environ.get('SECRET_KEY')
generate_url_controller = GenerateUrlController(secret_key)
show_password_controller = ShowPasswordController(secret_key)


def handler(event):
    if event['httpMethod'] == 'POST' and event['path'] == '/generate_url':
        body = json.loads(event['body'])
        response = generate_url_controller.generate_url(body)
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body'])
        }
    elif event['httpMethod'] == 'POST' and event['path'] == '/password':
        body = json.loads(event['body'])
        response = show_password_controller.show_password(body)
        return {
            'statusCode': response['statusCode'],
            'body': json.dumps(response['body'])
        }
    else:
        response = {
            'statusCode': 404,
            'body': json.dumps({'message': 'Route not found'})
        }
        return response
