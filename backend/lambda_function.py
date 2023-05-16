import json
from app.models.PasswordModel import RequestPassword
from app.service.GeneratePassword import PasswordGenerator
from app.service.GetUserId import GetUserId
from app.service.GetPasswordById import GetPasswordById

def lambda_handler(event, context):
    httpMethod = event['httpMethod']
    
    if httpMethod == 'POST':
        json_string = event['body']
        json_data = json.loads(json_string)
        
        request_password = RequestPassword(
            email=json_data['email'],
            password=json_data['password'],
            max_views=json_data['max_views'],
            valid_days=json_data['valid_days'],
            use_symbols=json_data['use_symbols'],
            use_numbers=json_data['use_numbers'],
            use_words=json_data['use_words'],
            length=json_data['length']
        )
        
        p = PasswordGenerator()
        password_data = p.generate_password_data(request_password=request_password)
    
        if password_data:
            return {
                'statusCode': 200,
    			'message':'Password criado com sucesso',
    			'response': 'ok'
            }
        else:
            return {
                'statusCode': 400,
    			'message':'Problema ao criar password',
    			'response': ''
            }

    if httpMethod == 'GET':
        json_string = event['body']
        json_data = json.loads(json_string)

        if json_data['get_url']:
            # aqui o front faz a requisição pro back passando o parametro {get_url: true} 
            # e retorna o id do user para que o front monte uma URL passando o id como parâmetro
            # {
            #     'email': "netto@netto.com",
            #     'get_url': true
            # }

            user_id = GetUserId.get_id(email=json_data['email'])

            if user_id:
                return {
                    'statusCode': 200,
                    'message':'Sucesso',
                    'user_id': user_id
                }
            else:
                return {
                    'statusCode': 400,
                    'message':'Usuário não encontrado',
                    'response': ''
                }
            
        if json_data['get_password']:
             # aqui o front faz a requisição pro back passando o parametro {get_password: true} 
            # e retorna o password do user para que o front
            # {
            #     'email': "netto@netto.com",
            #     'password': true
            #     'user_id': 'l234o2i3423'
            # }

            password = GetPasswordById.get_password(id=json_data['user_id'])

            if password:
                return {
                    'statusCode': 200,
                    'message':'Sucesso',
                    'password': password
                }
            else:
                return {
                    'statusCode': 400,
                    'message':'Usuário ou email não encontrado',
                    'response': ''
                }
            
