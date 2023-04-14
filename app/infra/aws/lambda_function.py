import json

from app.domain.use_cases import GeneratePasswordUseCase, GetPasswordUrlUseCase, RetrievePasswordUseCase, ValidatePasswordUseCase
from app.adapters.controllers import PasswordController
from app.infra.aws.dynamodb.dynamodb_password_repository import DynamoDBPasswordRepository
from app.domain.entities.password import Password

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']
    body = event['body'] or {}

    repository = DynamoDBPasswordRepository()

    generate_pass = GeneratePasswordUseCase(repository)

    controller = PasswordController( generate_pass )

    if method == 'POST' and path == '/password':
        password = Password(**json.loads(body))
        response = controller.generate_password(password)
        return {
            'statusCode': 201,
            'body': json.dumps(response.__dict__)
        }

    elif method == 'DELETE' and path == '/password':
        url = event['pathParameters']['url']
        response = controller.delete_password(url)
        return {
            'statusCode': 204,
            'body': json.dumps(response.__dict__)
        }

    elif method == 'GET' and path == '/password':
        url = event['pathParameters']['url']
        response = controller.get_password_by_url(url)
        return {
            'statusCode': 200,
            'body': json.dumps(response.__dict__)
        }

    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Route not found'})
        }
