import http.client
import ast
import json
import time
from cryptography.fernet import Fernet

def doUpdate():

    # Call the GET method
    conn = http.client.HTTPSConnection("rc53thwdg5.execute-api.ap-southeast-2.amazonaws.com")
    conn.request("GET", "/Prod/route53")
    r1 = conn.getresponse()

    # Convert the byte array of the response body to a dictionary
    bytedata = r1.read()
    dict_str = bytedata.decode("UTF-8")
    data = ast.literal_eval(dict_str)
    addressMatch = data['sourceIp'] == data['r53_ip']
    updateRequired = not addressMatch

    print('--------------------------------------------')
    print('GET response data')
    print('--------------------------------------------')
    print(r1.status, r1.reason)
    print(f'Source IP:         {data["sourceIp"]}')
    print(f'Route 53 address:  {data["r53_ip"]}')
    print(f'Address match:     {addressMatch}')
    print(f'Update required:   {updateRequired}')

    # Do update (if required)
    if updateRequired:
        # load the key
        try:
            with open('client/secret.key','rb') as mykey:
                key = mykey.read()    
        except:
            with open('secret.key','rb') as mykey:
                key = mykey.read()            

        # encrypt the data
        f = Fernet(key)
        encrypted = f.encrypt(data["sourceIp"].encode('utf-8'))

        # ####################################
        # Post encrypted data

        # Call the POST method

        conn = http.client.HTTPSConnection("rc53thwdg5.execute-api.ap-southeast-2.amazonaws.com")
        conn.request("POST", "/Prod/route53", json.dumps({ 'data': encrypted.decode("UTF-8") }))
        r1 = conn.getresponse()

        # ####################################
        # Process post response

        # Convert the byte array of the response body to a dictionary
        bytedata = r1.read()
        dict_str = bytedata.decode("UTF-8")
        data = ast.literal_eval(dict_str)

        print('--------------------------------------------')
        print('POST response data')
        print('--------------------------------------------')
        print(r1.status, r1.reason)
        print(f'Source IP:         {data["sourceIp"]}')
        print(f'Route 53 address:  {data["r53_ip"]}')
        print(f'Authorised:        {data["authorised"]}')

# ##########################################
# Run the doUpdate function

while True:
    doUpdate()
    time.sleep(60*10) # 10 minutes update interval