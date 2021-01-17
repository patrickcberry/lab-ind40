import json
import boto3
import ast
from cryptography.fernet import Fernet

def lambda_handler(event, context):

    # Extract the HTTP method
    httpMethod = event['httpMethod']

    # Extract Route 53 data
    client = boto3.client('route53')
    resorce_record_sets = client.list_resource_record_sets(
        HostedZoneId='Z9XC7GLI4YJJ6',
        MaxItems='1'
    )

    # Extract IP addresses
    sourceIp = event['requestContext']['identity']['sourceIp']
    r53_A_record_ip_value = resorce_record_sets["ResourceRecordSets"][0]["ResourceRecords"][0]["Value"]

    getResponse = {
        "name": 'Dyn DNS Route 53 Updater',
        "sourceIp": event['requestContext']['identity']['sourceIp'],
        "r53_ip": r53_A_record_ip_value,
        "httpMethod": "GET"        
    }

    # GET Method - return status data only
    if httpMethod == 'GET':
        return {
            "statusCode": 200,
            "body": json.dumps(getResponse)
        }

    # ##################################################################################
    # POST Method - update R53 A record (if valid request)
    elif httpMethod == 'POST':

        # actionStatus = "NONE"

        body_str = event['body']
        #print('body_str')
        #print(body_str)
        body = ast.literal_eval(body_str)
        #print('body')
        #print(body)
        client_encrypted = body['data'].encode('utf-8')
        #print('client_encrypted')
        #print(client_encrypted)

        # 
        with open('secret.key','rb') as mykey:
            key = mykey.read()     
        f = Fernet(key)
        # server_encrypted = f.encrypt(json.dumps(getResponse).encode('utf-8'))
        server_encrypted = f.encrypt(sourceIp.encode('utf-8'))

        print('Key')
        print(key)
        print(client_encrypted)
        print(len(client_encrypted))
        print(server_encrypted)
        print(len(server_encrypted))


        decrypted = f.decrypt(body['data'].encode('utf-8'))
        print(f'Decrypted:     {decrypted}')

        if decrypted.decode('utf-8') == sourceIp:
            authorised = 'True'
        else:
            authorised = 'False'

        if authorised:

            # Update Route 53
            response = client.change_resource_record_sets(
                HostedZoneId='Z9XC7GLI4YJJ6',
                ChangeBatch={
                    'Comment': 'string',
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': 'pblab.xyz',
                                'Type': 'A',
                                'TTL': 60,
        #                        'Region': 'ap-southeast-1',
                                'ResourceRecords': [
                                    {
                                        'Value': sourceIp
                                    },
                                ]
                            }
                        },
                    ]
                }
            )

            # Readback values from Route 53
            resorce_record_sets = client.list_resource_record_sets(
                HostedZoneId='Z9XC7GLI4YJJ6',
                MaxItems='1'
            )
            r53_A_record_ip_value = resorce_record_sets["ResourceRecordSets"][0]["ResourceRecords"][0]["Value"]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "name": 'Dyn DNS Route 53 Updater',
                # "actionStatus": actionStatus,
                "sourceIp": event['requestContext']['identity']['sourceIp'],
                "r53_ip": r53_A_record_ip_value,
                # "httpMethod": httpMethod,
                "authorised": authorised
            }),
        }

    else:
        # Request method not supported
        return {
            "statusCode": 501,
            "body": json.dumps({
                "name": 'Dyn DNS Route 53 Updater',
                "sourceIp": event['requestContext']['identity']['sourceIp'],
                "r53_ip": r53_A_record_ip_value,  
                "httpMethod": httpMethod,
                "error": 'HTTP method not supported'
            })
        }

