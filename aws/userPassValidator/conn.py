import boto3
import uuid
import datetime

class Database:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.userTable = self.dynamodb.Table('users')
        self.passTable = self.dynamodb.Table('userpass')
    
    def calculate_passlifetime(passlifetime):
        epoch_now = int(datetime.datetime.now().timestamp())
        passlifetime_seconds = int(passlifetime * 3600)  # Convert hours to seconds
        epoch_passlifetime = epoch_now + passlifetime_seconds
        return epoch_passlifetime
    
    def put_item(self, user, password):
        try:
            user_id = int(uuid.uuid4())
            user['userid'] = user_id
            self.table.put_item(Item=user)
            
            passlifetime = self.calculate_passlifetime(userpass_item['passlifetime'])
            
            userpass_item = {
                'userid': user_id,
                'passid': int(uuid.uuid4()),
                'passlifetime': passlifetime,
                'passlimitview': password.passlimitview,
                'currentlink': password.linkdata,
                'status': 1,
            }

            try:
                self.table.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(userid) and attribute_not_exists(passid)')
                return {'result': 'OK', 'err_code': 0, 'data': 'Dados registrados com sucesso'}
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ConditionalCheckFailedException':
                    return {'result': 'ERRO', 'err_code': 1, 'data': 'Já existe um usuário com esse userid ou passid'}
                else:
                    return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar item: {str(e)}"}

        except Exception as e:
            return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar item: {str(e)}"}
    
            
    def update_userpass(self, user_id, pass_id, passlimitview):
        """Esse método serve para atualizar na medida em que o usuário clica no link"""
        response = self.passTable.update_item(
            Key={
                'userid': user_id,
                'passid': pass_id
            },
            UpdateExpression='set passlimitview = :v',
            ExpressionAttributeValues={
                ':v': passlimitview
            }
        )
        
    def user_query(self, login):
        """ Metodo para realizar a consulta dos usuários e dos passwords
            Melhorar esse método para permitir salvar um usuário caso ele não exista na base
        """
        user_response = self.userTable.query(
            KeyConditionExpression='login = :login',
            ExpressionAttributeValues={
                ':login': login
            }
        )
        
        user_items = user_response['Items']
         
        if len(user_items) == 0:
            return {'result': 'WARNING', 'err_code': '0', 'data': 'Login não encontrato'}
        
        userpass_response = self.passTable.query(
            IndexName='userid-index',
            KeyConditionExpression='userid = :userid',
            ExpressionAttributeValues={
                ':uid': user_items.userid,
            }
        )
        userpass_items = userpass_response['Items']
        
        if len(userpass_items) == 0:
            return {'result': 'WARNING', 'err_code': '0', 'data': 'O login foi identificado mas há um erro no cadastro'}
        
        user_items = user_response['Items']
        
        return  user_items