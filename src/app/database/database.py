import boto3
from boto3.dynamodb.conditions import Key, Attr


class Database:
    def __init__(self, table_name):
        self.table_name = table_name

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="sa-east-1",
            endpoint_url="http://localhost:4577",
            aws_access_key_id='test',
            aws_secret_access_key='test',
            verify=False,
        )

        self.table = self.dynamodb.Table(self.table_name)

    def insert_one(self, password_data):
        self.table.put_item(Item=password_data)

    def find_one(self, password_uuid, code):
        response = self.table.query(
            KeyConditionExpression=Key("id").eq(password_uuid) & Key("code").eq(code)
        )
        items = response.get("Items", [])
        return items[0] if items else None

    def delete_one(self, uuid, code):
        self.table.delete_item(
            Key={
                'id': uuid,
                'code': code
            }
        )

    def update_one(self, uuid, code, update_expression):
        self.table.update_item(
            Key={
                'id': uuid,
                'code': code
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues={':val': 1},
            ConditionExpression=Attr('views_left').gt(0),  # Prevent negative views_left
        )