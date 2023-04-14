import os
import boto3
from typing import Optional
from boto3.dynamodb.conditions import Key
from app.domain.entities.password import Password
from app.domain.repositories.password_repository import PasswordRepository

class DynamoDBPasswordRepository(PasswordRepository):
    def __init__(self, table_name: str = "passwords"):
        dynamodb = boto3.resource("dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT_URL"))
        self.table = dynamodb.Table(table_name)

    def save_password(self, password: Password) -> None:
        item = {
            "url": password.url,
            "password": password.password,
            "max_views": password.visualizations_limit,
            "expiration_time": password.valid_until,
            "views_count": password.views_count,
        }
        return self.table.put_item(Item=item)

    def get_password_by_url(self, url: str) -> Optional[Password]:
        response = self.table.query(KeyConditionExpression=Key("url").eq(url))
        items = response.get("Items", [])
        if not items:
            return None
        item = items[0]
        return Password(
            password=item["password"],
            visualizations_limit=item["max_views"],
            valid_until=item["expiration_time"],
        )
    
    def get_password(self, password: str) -> Optional[Password]:
        response = self.table.scan(FilterExpression=Key("password").eq(password))
        items = response.get("Items", [])
        if not items:
            return None
        item = items[0]
        return Password(
            password=item["password"],
            visualizations_limit=item["max_views"],
            valid_until=item["expiration_time"],
        )

    def delete_password(self, password: Password) -> None:
        key = {"url": password.url}
        self.table.delete_item(Key=key)
