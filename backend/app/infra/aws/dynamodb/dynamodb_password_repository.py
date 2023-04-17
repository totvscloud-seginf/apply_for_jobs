import os, datetime
import boto3
from typing import Optional
from boto3.dynamodb.conditions import Key
from app.domain.entities.password import Password
from app.domain.repositories.password_repository import PasswordRepository
from app.domain.exceptions.password_not_found_error import PasswordNotFoundError

class DynamoDBPasswordRepository(PasswordRepository):
    def __init__(self, table_name: str = "passwords"):
        dynamodb = boto3.resource(
            "dynamodb", 
            endpoint_url=os.environ.get("DYNAMODB_ENDPOINT_URL"),
            region_name='us-east-1'
        )
        self.table = dynamodb.Table(table_name)

    def save_password(self, password: Password) -> None:
        item = {
            "id": password.id,
            "password": password.password,
            "max_views": password.visualizations_limit,
            "expiration_time": int( password.valid_until ) if password.valid_until is not None else '',
            "views_count": password.views_count,
        }
        return self.table.put_item(Item=item)
    
    def add_password_views_count(self, item, views_count: int) -> None:
        views_count += 1
        return self.table.update_item(
            Key={
                'id': item['id'],
                'password': item['password']
            },
            UpdateExpression="set views_count = :v",
            ExpressionAttributeValues={
                ':v': views_count
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_password_by_id(self, id: str) -> Optional[Password]:
        response = self.table.query(KeyConditionExpression=Key("id").eq(id))
        items = response.get("Items", [])
        if not items:
            raise PasswordNotFoundError(id)
        
        item = items[0]
        if self.add_password_views_count(item, item['views_count'])['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise PasswordNotFoundError(id)

        return Password(
            id=item['id'],
            password=item['password'],
            visualizations_limit=item['max_views'],
            valid_until= item['expiration_time'] if item['expiration_time'] else None,
            views_count=item['views_count']
        )

    def delete_password(self, password: Password) -> None:
        self.table.delete_item(Key={"id": password.id, "password": password.password})
