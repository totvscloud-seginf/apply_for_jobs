import json, logging
from datetime import datetime
from dotenv import load_dotenv

from app.domain.entities.password import Password
import app.domain.use_cases.password_use_case as use_cases
from app.adapters.controllers.password_controller import PasswordController
from app.infra.aws.dynamodb.dynamodb_password_repository import DynamoDBPasswordRepository

load_dotenv()
repository = DynamoDBPasswordRepository()
generate_pass = use_cases.PasswordUseCase( repository )
controller = PasswordController( generate_pass )


"""
This function is called when a POST request is made to the /password/{id} endpoint
"""
def set_password(event, context) -> dict:
    # Get the request body
    body = event['body'] or {}
    request = json.loads(body)

    # Create a Password object
    password = Password(
        password=request['password'],
        visualizations_limit=request['view_limit'],
        valid_until=datetime.timestamp(datetime.now()) + (int(request['valid_until']) * 86400) if request['valid_until'] else None,
    )

    # Generate the password
    try:
        response = controller.set_password(password)
        return {
            'statusCode': 201,
            'body': json.dumps( response.__dict__, default=str )
        }
    except:
        logging.error(
            'Invalid password', 
            exc_info=True, 
            stack_info=True, 
            extra={
                'password': password.password
            }
        )
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid password'})
        }

"""
This function is called when a GET request is made to the /password/{id} endpoint
"""
def get_password(event, context) -> dict:
    id = event['pathParameters']['id'] # Get the id from the path 

    # Check if the id is empty or not
    if not id:
        # If the id is empty, return a HTTP 404 status code with a message
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Password not found',
            })
        }

    try:
        response = controller.get_password_by_id(id) # Get the password from the database
        return {
            'statusCode': 200, # Return a HTTP 200 status code
            'body': json.dumps( response.__dict__, default=str ) if type(response) == Password else response # Return the password in JSON format
        }
    except Exception as e:
        logging.error(
            'Password not found',
            exc_info=True,
            stack_info=True,
            extra={
                'id': id
            }
        )
        # If any other error occurs, return a HTTP 404 status code with a message
        return {
            "isBase64Encoded": False,
            'statusCode': 404,
            'body': json.dumps({'message': 'Password not found', 'error': str(e)})
        }

"""
This function is called when a DELETE request is made to the /password/{id} endpoint
"""
def delete_password(event, context) -> dict:
    # The id of the password is passed in the path parameters
    id = event['pathParameters']['id']

    try:
        # Delete the password with the given id
        response = controller.delete_password(id)
        # Return the response with status code 204
        return {
            'statusCode': 204,
            'body': json.dumps(response.__dict__, default=str)
        }
    except:
        logging.error(
            'Password not found',
            exc_info=True,
            stack_info=True,
            extra={
                'id': id
            }
        )
        # If the password is not found return status code 404
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Password not found'})
        }