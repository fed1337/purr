"""
Helper script to generate random values for Lemur configuration
"""
from base64 import urlsafe_b64encode
from os import urandom
from secrets import choice, token_hex
from string import ascii_lowercase, ascii_uppercase, digits

chars = ascii_uppercase + ascii_lowercase + digits + "~!@#$%^&*()_+"

print("LEMUR_ENCRYPTION_KEY:", urlsafe_b64encode(urandom(32)).decode())
print("LEMUR_TOKEN_SECRET:", ''.join(choice(chars) for x in range(24)))
print("SECRET:", token_hex())
