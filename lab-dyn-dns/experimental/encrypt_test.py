from cryptography.fernet import Fernet

# Generate key and write to file
key = Fernet.generate_key()
with open('experimental/secret.key','wb') as mykey:
    mykey.write(key)

# Read key back
with open('experimental/secret.key','rb') as mykey:
    key = mykey.read()

f = Fernet(key)

text = 'This is the original text'
encrypted = f.encrypt(text.encode('utf-8'))
decrypted = f.decrypt(encrypted).decode()

print()
print(f'Original:   {text}')
print(f'Encrypted:  {encrypted}')
print(f'Decrypted:  {decrypted}')

isequal = text == decrypted

print(f'Is equal:   {isequal}')

