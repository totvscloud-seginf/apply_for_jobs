import app.infra.aws.dynamodb.dynamodb_manager as db_manager
import app.infra.aws.lambda_function.handler as lambda_function
from dotenv import load_dotenv


def lambda_handler(event, context):
    return lambda_function.get_password(event, context)  # call the handler function from lambda_function.py

if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env.
    db_manager.DynamoDBManager().create_table() # create table