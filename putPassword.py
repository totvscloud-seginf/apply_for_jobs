import json
import boto3
from uuid import uuid4
import datetime
import base64
import string
import secrets

def lambda_handler(event, context):
    password=""
    generate_password=False
    password_chars=string.ascii_letters + string.digits + string.punctuation
    password_length=12
    
    req_body = get_body(event)
    try:
        password = str(req_body["password"])
    except Exception:
        pass
    try:
        if req_body["generate_password"]:
            generate_password=req_body["generate_password"]
    except Exception:
        pass
    try:
        if req_body["password_chars"]:
            password_chars=str(req_body["password_chars"])
    except Exception:
            pass
    try:
        if req_body["password_length"]:
            password_length=int(req_body["password_length"])
    except Exception:
        pass
    
    if password == '':
        if not generate_password:
            return {
                'statusCode': 400,
                'body': "NO PASSWORD SUPPLIED"
            }
        password = password_gen(password_chars,password_length)
    
    try:
        view_limit = int(req_body["view_limit"])
    except Exception(e):
        return {
        'statusCode': 400,
        'body': "INVALID VIEW LIMIT SUPPLIED"
        }
    if view_limit < 1:
        return {
        'statusCode': 400,
        'body': "NEGATIVE VIEW LIMIT SUPPLIED"
        }
    try:
        days_limit = int(req_body["days_limit"])
    except Exception:
        return {
        'statusCode': 400,
        'body': "INVALID OR NO TIME LIMIT SUPPLIED"
        }
    if days_limit < 0:
        return {
        'statusCode': 400,
        'body': "INVALID OR NO TIME LIMIT SUPPLIED"
        }
    try:
        time_limit = validate_time(req_body["time_limit"],days_limit)
    except Exception:
        raise
        return {
        'statusCode': 400,
        'body': "INVALID OR NO TIME LIMIT SUPPLIED"
        }
    rand_token = str(uuid4())
    client = boto3.client('dynamodb')
    data = client.put_item(
        TableName='PasswordTable',
        Item={
            'id': {
                'S': rand_token
            },
            'password': {
                'S': password
            },
            'view_limit': {
                'N': str(view_limit)
            },
            'time_limit': {
                'N': str(time_limit)
            }
        }
    )
    body = {
      'token':rand_token,
      'view_limit':view_limit,
      'time_limit':time_limit
    }
    response = {
      'statusCode': 200,
      'body': json.dumps(body),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
    }
  
    return response

def validate_time(time_str,days=0):
    now = datetime.datetime.now()
    time_limit = datetime.datetime.strptime(time_str, '%Hh%Mm%Ss').time()
    time_limit_timedelta = datetime.timedelta(days=days, seconds=time_limit.second, minutes=time_limit.minute, hours=time_limit.hour) 
    time_limit_sum = now + time_limit_timedelta
    time_limit_ts = int(datetime.datetime.timestamp(time_limit_sum))

    return time_limit_ts

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

def password_gen(chars,length):
    password = ""
    for i in range(length):
        password += ''.join(secrets.choice(chars))
    return password
