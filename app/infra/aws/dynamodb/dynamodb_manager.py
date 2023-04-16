import boto3
import os

class DynamoDBManager():
    def __init__(self):
        self.table_name = 'passwords'
        self.dynamodb = boto3.resource(
            'dynamodb', 
            endpoint_url=os.environ.get("DYNAMODB_ENDPOINT_URL"),
            region_name='us-east-1'
        )

    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'url',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'password',
                        'KeyType': 'RANGE'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'url',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'password',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            return table
        except boto3.client('dynamodb').exceptions.ResourceInUseException:
            return None
    
    def delete_table(self):
        self.dynamodb.Table(self.table_name).delete()
