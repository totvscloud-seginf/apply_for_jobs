import boto3
import time
from botocore.exceptions import ClientError

class GetPasswordById:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_password(self, id):
        try:
            response = self.table.get_item(Key={'id': id})

            can_view = self.can_view(self, response.get('num_views'), response.get('max_views'), response.get('valid_until') )
            
            password = response.get('password')
            
            if can_view:
                return password
            else:
                return None
        except ClientError as e:
            print(f"Erro ao buscar senha do email")
            return None
        
    def can_view(self, num_views, max_views, valid_until ):
        return num_views < max_views and time.time() < valid_until
    