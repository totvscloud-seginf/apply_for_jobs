import boto3
from botocore.exceptions import ClientError

class SavePassword:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_password(self, password_data:dict):
        try:
            self.table.put_item(Item=password_data)
            return True
        except ClientError as e:
            print(f"Erro ao salvar senha do email {password_data['email']}: {e.response['Error']['Message']}")
            return False