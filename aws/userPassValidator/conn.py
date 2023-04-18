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
          
            
            pass_ = password['password']
            
           
            
            hash_object = hashlib.md5(str(pass_).encode())
            hash_hex = hash_object.hexdigest()
            pass_id = hash_hex
            
            
            userpass_item = {
                'passid': pass_id,
                'userid': user_id,
                'password': str(base64.b64encode(password['password'].encode("utf-8"))),
                'passlifetime': int(passlifetime),
                'passlimitview': int(password['passlimitview']),
                'currentlink': str(password['currentlink'])
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
       
    
    def add_new_pass(self, user_id, newpass):
        passlifetime = self.calculate_passlifetime(newpass['passlifetime'])
        userpass_item = {
                'userid': user_id,
                'passid': int(uuid.uuid4()),
                'password':  base64.b64encode(newpass.password.encode("utf-8")),
                'passlifetime': passlifetime,
                'passlimitview': newpass.passlimitview,
                'currentlink': newpass.linkdata,
            }
        
        try:
            self.passTable.put_item(Item=userpass_item, ConditionExpression='attribute_not_exists(userid) and attribute_not_exists(passid)')
            return {'result': 'OK', 'err_code': 0, 'data': 'Novo password adicionado'}
        except Exception as e:
              return {'result': 'ERRO', 'err_code': 1, 'data': f"Erro ao adicionar password: {str(e)}"}

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
    
    def user_query(self, login):
        """ Metodo para realizar a consulta dos usuários e dos passwords
            Melhorar esse método para permitir salvar um usuário caso ele não exista na base
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
            return {'result': 'WARNING', 'err_code': '1000', 'data': 'Login não encontrato'}
        
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
                'currentlink': items['currentlink'] 
            }
        
            userpass_items.append(item_dict)
  
        return userpass_items[0]