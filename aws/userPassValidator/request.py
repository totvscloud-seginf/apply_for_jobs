import json
from user import user

usuario = user()
 
def lambda_handler(event, context):
    proxy = event['pathParameters']['proxy']
    
    if proxy == 'do_save_new_user':
        data_body = event['body']
        return new_user(event, json.loads(data_body))
        
    elif proxy == 'do_user_login':
        data_body = event['body']
        return user_login(event, json.loads(data_body))
        
    elif proxy == 'do_user_link_gen':
        data_body = event['body']
        return get_link(event, json.loads(data_body))
        
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method not allowed')
        }
        
def user_login(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('teste')
    }

def new_user(event, context):
    response = usuario.do_save_new_user(context)
    return {
        'statusCode': 200,
        'body': json.dumps({"resp" : response})
    }
    
def get_link(event, context):
    response = usuario.do_user_get_link(context)
    return {
        'statusCode': 200,
        'body':  json.dumps({"resp" : response})
    }