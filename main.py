from app.infra.aws.dynamodb import DynamoDBManager
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env.
    DynamoDBManager().create_table() # create table