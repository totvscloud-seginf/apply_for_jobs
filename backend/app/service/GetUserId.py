import boto3
from botocore.exceptions import ClientError

class GetUserId:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_id(self, email):
        try:
            response = self.table.get_item(Key={'email': email})
            item = response.get('id')
            if item:
                return item.get('id')
            else:
                return None
        except ClientError as e:
            print(f"Erro ao buscar senha do email {email}: {e.response['Error']['Message']}")
            return None