import json

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps({
            "name": 'who_am_i',
            "sourceIp": event['requestContext']['identity']['sourceIp']
        }),
    }
