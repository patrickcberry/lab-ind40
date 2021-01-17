# Generate a random string (for a shared secret)

import secrets

key = secrets.token_urlsafe(1024)
print(key)