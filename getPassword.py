import json
import boto3
import base64

def lambda_handler(event, context):
    table_name='PasswordTable'
    print(f'event: {json.dumps(event)}')
    req_body = event
    password_id=""
    try:
        password_id = str(req_body["pathParameters"]["token"])
        password_id = password_id.lstrip(r'/')
    except Exception:
        return {
            'statusCode': 400,
            'body': "NO PASSWORD_ID SUPPLIED"
        }
    if password_id == '':
        return {
            'statusCode': 400,
            'body': "NO PASSWORD_ID SUPPLIED"
        }
    
    client = boto3.client('dynamodb')
    data = ""
    try:
        data = client.update_item(
            TableName=table_name,
            Key={
                'id': {'S': password_id}
            },
            UpdateExpression=f'SET view_limit = view_limit - :dec',
            ExpressionAttributeValues={
                ':dec': {'N': '1'}
            },
            ReturnValues= "ALL_NEW"
        )
    except Exception:
        return id_not_found_handler(password_id)
    
    item = data['Attributes']
    password = item['password']['S']
    view_limit = int(item['view_limit']['N'])
    time_limit = int(item['time_limit']['N'])
    body = {
      'token':password_id,
      'password':password,
      'view_limit':view_limit,
      'time_limit':time_limit
    }
    if view_limit < 1:
        data = client.delete_item(
            TableName=table_name,
            Key={
                'id': {'S': password_id}
            }
        )
    
    response = {
      'statusCode': 200,
      'body': json.dumps(body),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
    }
  
    return response


def get_body(event):
    body = ""
    try:
        body_json = event['body']
        if event['isBase64Encoded']:
            body_json = base64.b64decode(body_json)
        body = json.loads(body_json)
    except Exception:
        raise
    return body

def id_not_found_handler(password_id):
    body = {
      'token':password_id,
    }
    response = {
      'statusCode': 404,
      'body': json.dumps(body),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
    }
    return response
