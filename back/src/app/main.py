import json
import boto3

from back.src.app.controller.generate_url_controller import GenerateUrlController
from back.src.app.controller.show_password_controller import ShowPasswordController
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

ssm = boto3.client('ssm', region_name='sa-east-1')

private_key = serialization.load_pem_private_key(
    ssm.get_parameter(Name='PRIVATE_KEY', WithDecryption=True)['Parameter']['Value'].encode('utf-8'),
    password=ssm.get_parameter(Name='PRIVATE_KEY_PASSWORD', WithDecryption=True)['Parameter']['Value'].encode('utf-8'),
    backend=default_backend()
)
public_key = serialization.load_pem_public_key(
    ssm.get_parameter(Name='PUBLIC_KEY', WithDecryption=True)['Parameter']['Value'].encode('utf-8'),
    backend=default_backend()
)
generate_url_controller = GenerateUrlController(public_key)
show_password_controller = ShowPasswordController(private_key)


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
