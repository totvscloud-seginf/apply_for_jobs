import boto3
import uuid
import datetime
import base64

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
            self.userTable.put_item(Item=user)
            
            passlifetime = self.calculate_passlifetime(password['passlifetime'])
            
            userpass_item = {
                'userid': user_id,
                'passid': int(uuid.uuid4()),
                'password':  base64.b64encode(password.password.encode("utf-8")),
                'passlifetime': passlifetime,
                'passlimitview': password.passlimitview,
                'currentlink': password.linkdata,
                'status': 1,
            }

            try:
                self.passTable.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(userid) and attribute_not_exists(passid)')
                return {'result': 'OK', 'err_code': 0, 'data': 'Dados registrados com sucesso'}
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ConditionalCheckFailedException':
                    return {'result': 'ERRO', 'err_code': 1, 'data': 'Já existe um usuário com esse userid ou passid'}
                else:
                    return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar usuário: {str(e)}"}

        except Exception as e:
            return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar usuário: {str(e)}"}
    
    def add_new_pass(self, user_id, newpass):
        
        passlifetime = self.calculate_passlifetime(newpass['passlifetime'])
        userpass_item = {
                'userid': user_id,
                'passid': int(uuid.uuid4()),
                'password':  base64.b64encode(newpass.password.encode("utf-8")),
                'passlifetime': passlifetime,
                'passlimitview': newpass.passlimitview,
                'currentlink': newpass.linkdata,
                'status': 1,
            }
        
        try:
            self.passTable.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(userid) and attribute_not_exists(passid)')
            return {'result': 'OK', 'err_code': 0, 'data': 'Novo password adicionado'}
        except Exception as e:
              return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar password: {str(e)}"}

    def update_userpass_limitview(self, user_id, pass_id, passlimitview):
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

        return {'result': 'OK', 'err_code': 0, 'data': "limite atualizado com sucesso"}
    
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
            return {'result': 'WARNING', 'err_code': '1000', 'data': 'Login não encontrato'}
        
        userpass_response = self.passTable.query(
            IndexName='userid-index',
            KeyConditionExpression='userid = :userid and password = :password',
            ExpressionAttributeValues={
                ':uid': user_items.userid,                
            }
        )

        userpass_items = userpass_response['Items']
        
        if len(userpass_items) == 0:
            return {'result': 'WARNING', 'err_code': '2000', 'data': 'Senha não cadastrada'}
        
        return  userpass_items