import json
import re
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
        
    elif proxy == 'do_user_get_link':
        data_body = event['body']
        return get_link(event, json.loads(data_body))
    elif proxy == 'do_user_set_new_pass':
        data_body = event['body']
        return set_new_pass(event, json.loads(data_body))
    else:
        if 'use_key' in proxy and 'user_x' in proxy:
            data_body = json.loads(event['body'])
            #separando os dados do link...
            #match_user_x = re.search(r'user_x=([^&]*)', proxy)
            #match_user_key = re.search(r'use_key=([^&]*)', proxy)
            #user_x = match_user_x.group(1) if match_user_x else None
            #use_key = match_user_key.group(1) if match_user_key else None
            
            data_body['password']['url'] = proxy
            
            return use_link(event, data_body)
        else:
            return {
                'statusCode': 400,
                 'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': 'Url Inválida'
            }
        
def user_login(event, context):
    response = usuario.do_user_login(context)
    return {
        'statusCode': 200,
         'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({'resp' : response})
    }

def new_user(event, context):
    response = usuario.do_save_new_user(context)
    return {
        'statusCode': 200,
         'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({"resp" : response})
    }
    
def get_link(event, context):
    response = usuario.do_user_get_link(context)
    return {
        'statusCode': 200,
         'headers': {
            
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':  json.dumps({"resp" : response})
    }

def use_link(event, context):
    response = usuario.do_user_use_link(context)
    return {
        'statusCode': 200,
         'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':  json.dumps({"resp" : response})
    }

def set_new_pass(event, context):
    response = usuario.do_user_add_newpass(context)
    return {
        'statusCode': 200,
         'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':  json.dumps({"resp" : response})
    }
