import json
from user import user

def lambda_handler(event, context):
    
    if event['rawPath']  == "/do_user_login":
        dados = event['body']
        return {'teste': 'do_user_login', 
                 'body': json.loads(dados)
                }

    elif event['rawPath']  == "/do_save_new_user":
        dados = event['body']
        return {'teste': 'do_save_new_user', 
                 'body': json.loads(dados)
                }

    elif event['rawPath']  == "/do_user_link_gen":
        dados = event['body']
        return {'teste': 'deu certo', 
                 'body': json.loads(dados)
                }

    elif event['rawPath']  == "/do_user_password_view":
        dados = event['body']
        return {'teste': 'deu certo', 
                 'body': json.loads(dados)
                }
    
    elif event['rawPath']  == "/do_user_add_newpass":
        dados = event['body']
        return {'teste': 'deu certo', 
                 'body': json.loads(dados)
                }
       