import boto3
import hashlib
import datetime
import base64
import sys

sys.set_int_max_str_digits(0)

class Database:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.userTable = self.dynamodb.Table('users')
        self.passTable = self.dynamodb.Table('userpass')
    
    def calculate_passlifetime(self, passlifetime):
        epoch_now = int(datetime.datetime.now().timestamp())
        passlifetime_seconds = int(passlifetime * 3600)  # Convert hours to seconds
        epoch_passlifetime = epoch_now + passlifetime_seconds
        return epoch_passlifetime
    
    def user_exists(self, user_id):
        response = self.userTable.query(
            KeyConditionExpression='userid = :_userid',
            ExpressionAttributeValues={
                ':_userid': user_id
            }
        )
        return response.get('Count') > 0
    
    def get_hash_id(self, user):
        hash_object = hashlib.md5(str(user).encode())
        hash_hex = hash_object.hexdigest()
        return hash_hex
    
    def user_login(self, login, password):
        """ Metodo para realizar login
        """
        
        user_id = self.get_hash_id(login)
        pass_id = self.get_hash_id(password)
        
        user_response = self.userTable.query(
            KeyConditionExpression='userid = :userid and login = :login',
            ExpressionAttributeValues={
                ':login': login,
                ':userid': user_id
            }
        )
        
        user_items = user_response['Items']
        
        for item in user_response['Items']:
            userid = item.get('userid')
            
        if len(user_items) == 0:
            return [{'result': 'WARNING', 'err_code': '-1000', 'data': 'Login ou senha não encontrados'}]
        
        userpass_response = self.passTable.query(
            KeyConditionExpression='passid = :passid and userid = :userid',
            ExpressionAttributeValues={
                ':userid': userid,
                ':passid': pass_id
            }
        )
        
        if len(userpass_response) == 0:
            return [{'result': 'WARNING', 'err_code': '-1020', 'data': 'Login ou senha não encontrados'}]
        userpass_items = []
        for items in userpass_response['Items']:
            item_dict = {
                'passid': items['passid'],
                'userid': items['userid'],
                'password': items['password'],
                'passlifetime': int(items['passlifetime']),
                'passlimitview': int(items['passlimitview']),
                'currentlink': items['currentlink'],
                'passtatus' : int(items['passtatus'])
            }
        
            userpass_items.append(item_dict)

        return userpass_items

    def put_user(self, user, password):
        try:
            
            user_id = self.get_hash_id(user)
            
            passlifetime = self.calculate_passlifetime(int(password['passlifetime']))
            
            
            if self.user_exists(user_id):
                return {'result': 'ERRO', 'err_code': -200, 'data': 'Já existe um usuário com esse email'}
            
            _user = {
                'userid': user_id,
                'login' : str(user)
            }
          
            pass_id = self.get_hash_id(password['password'])
           
            
            userpass_item = {
                'passid': pass_id,
                'userid': user_id,
                'password': base64.b64encode(password['password'].encode("utf-8")).decode("utf-8"),
                'passlifetime': int(passlifetime),
                'passlimitview': int(password['passlimitview']),
                'currentlink': str(password['currentlink']),
                'passtatus' : 1
            }
            
            self.userTable.put_item(Item=_user)

            try:
                self.passTable.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(userid) and attribute_not_exists(passid)')
                return {'result': 'OK', 'err_code': 0, 'data': 'Dados registrados com sucesso'}
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ConditionalCheckFailedException':
                    return {'result': 'ERRO', 'err_code': -200, 'data': 'Já existe um usuário com esse userid ou passid'}
                else:
                    return {'result': 'ERRO', 'err_code': -300, 'data': f"Erro ao adicionar senha: {str(e)}"}
        except Exception as err:
            return {'result': 'ERRO', 'err_code': -100, 'data': f"Erro ao adicionar usuário: {str(err)}"}
       
    
    def add_new_pass(self, user_id, password):

        user = self.get_hash_id(user_id)
        
        if self.user_exists(user):
            query = self.user_query(user_id)

            for pass_check in query:
                if 'result' in pass_check:
                    return pass_check
                if pass_check['passtatus'] > 0:
                    pass_check['exists_valid_pass'] = 'True'
                    return pass_check
            
            pass_id = self.get_hash_id(password['password'])
            
            passlifetime = self.calculate_passlifetime(int(password['passlifetime']))
            
            userpass_item = {
                'passid': pass_id,
                'userid': user,
                
                'password': base64.b64encode(password['password'].encode('ascii')).decode('ascii'),
                'passlifetime': int(passlifetime),
                'passlimitview': int(password['passlimitview']),
                'currentlink': str(password['currentlink']),
                'passtatus' : int(1)
            }
             
            try:
                self.passTable.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(passid)')
                return {'result': 'OK', 'err_code': 0, 'data': 'Novo password adicionado'}
            except Exception as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ConditionalCheckFailedException':
                    return {'result': 'ERRO', 'err_code': -4200, 'data': 'O password antigo não pode ser reutilizado'}
                else:
                    return {'result': 'ERRO', 'err_code': -300, 'data': f"Erro ao adicionar senha: {str(e)}"}
        else:
            return {'result': 'WARNING', 'err_code': -3000, 'data': 'Login não encontrato'}

    def update_userpass_limitview(self, user_id, pass_id, passlimitview):
        """Esse método serve para atualizar na medida em que o usuário clica no link"""
        
        self.passTable.update_item(
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
    
    def update_password_status(self, user_id, pass_id):
       
        try:
            self.passTable.update_item(
                Key={
                    'userid': user_id,
                    'passid': pass_id
                    },
                    UpdateExpression='set passtatus = :v',
                    ExpressionAttributeValues={
                    ':v': int(0)
                    }
            )
            return {'result': 'OK', 'err_code': 0, 'data': 'Status atualizado com sucesso'}
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ConditionalCheckFailedException':
                return {'result': 'ERRO', 'err_code': -200, 'data': 'Status não atualizado'}
            else:
                return {'result': 'ERRO', 'err_code': -300, 'data': f"Erro ao atualizar status: {str(e)}"}

    def user_query(self, login):
        """ Metodo para realizar a consulta dos usuários e dos passwords
        """
        user_id = self.get_hash_id(login)
        
        user_response = self.userTable.query(
            KeyConditionExpression='userid = :userid and login = :login',
            ExpressionAttributeValues={
                ':login': login,
                ':userid': user_id
            }
        )
        
        user_items = user_response['Items']
        
        for item in user_response['Items']:
            userid = item.get('userid')
            
        if len(user_items) == 0:
            return [{'result': 'WARNING', 'err_code': '-1000', 'data': 'Login não encontrato'}]
        
        userpass_response = self.passTable.query(
            IndexName='userid-index',
            KeyConditionExpression='userid = :userid',
            ExpressionAttributeValues={
                ':userid': userid,                
            }
        )
        
        userpass_items = []
        
        for items in userpass_response['Items']:
            item_dict = {
                'passid': items['passid'],
                'userid': items['userid'],
                'password': items['password'],
                'passlifetime': int(items['passlifetime']),
                'passlimitview': int(items['passlimitview']),
                'currentlink': items['currentlink'],
                'passtatus' : int(items['passtatus'])
            }
        
            userpass_items.append(item_dict)
  
        return userpass_items