from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open('client/secret.key','wb') as mykey:
    mykey.write(key)

with open('server/route_53/secret.key','wb') as mykey:
    mykey.write(key)
