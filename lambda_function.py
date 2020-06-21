import pymysql
import datetime
import json
import base64
import os
#import sys

#RDS settings
with open('config.json', 'r') as f:
    config = json.load(f)

is_mysql_avail = True

try:
    conn = pymysql.connect(config['rds_host'], user=config['username'], passwd=config['password'], db=config['db_name'], connect_timeout=5)
except pymysql.MySQLError as e:
    print('ERROR CONNECTING MYSQL')
    #sys.exit()
    is_mysql_avail = False


def lambda_handler(event, context):
    
    target_url = event["queryStringParameters"]["link"]
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url
    
    userId = base64.b64encode(os.urandom(32))[:8].decode()
    cookie_max_age = 60 * 60 * 24 * 365 * 3  # 3 years
    
    try:
        headers = event["headers"]
        
        if 'cookie' in headers.keys():
            # parse cookies string
            cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in headers['cookie'].split('; ')}
            if 'userId' in cookies.keys():
                userId = cookies['userId']
        
        if is_mysql_avail:
            with conn.cursor() as cur:
                # Timestamp is entered automatically in table logic (default: CURRENT_TIMESTAMP)
                cur.execute("insert into redirect_log (target_url, user_id, request_header) VALUES (%s, %s, %s)", (target_url, userId, json.dumps(headers)))
            conn.commit()
    except:
        print('An unknown error occured')
        #pass  # don't let any error stop the redirecting itself
    
    return {
        'statusCode': 302,
        'body': f'Redirecting to {target_url}',
        'headers': {'location': target_url,
                    'Set-Cookie': 'userId=%s; Max-Age=%i' % (userId, cookie_max_age),
        }
    }