"""
Helper script to generate random values for Lemur configuration
"""

import secrets
import string
from base64 import b64encode, urlsafe_b64encode
from os import urandom
from secrets import choice, token_hex
from string import ascii_lowercase, ascii_uppercase, digits
from time import time

from cryptography.hazmat.primitives import hashes, hmac

chars = ascii_uppercase + ascii_lowercase + digits + "~!@#$%^&*()_+"


def get_random_secret(length):
    """Similar to get_pseudo_random_string, but accepts a length parameter."""
    return "".join(secrets.choice(chars) for x in range(length))


def generate_state_token():
    t = int(time())
    ts = hex(t)[2:].encode("ascii")
    h = hmac.HMAC(b64encode(get_random_secret(32).encode("utf8")), hashes.SHA256())
    h.update(ts)
    digest = b64encode(h.finalize())
    state = ts + b":" + digest
    return state.decode()


print("LEMUR_ENCRYPTION_KEY:", urlsafe_b64encode(urandom(32)).decode())
print("LEMUR_TOKEN_SECRET:", "".join(choice(chars) for x in range(24)))
print("SECRET:", token_hex())
print("OAUTH2_SECRET:", token_hex())
print("OAUTH_STATE_TOKEN_SECRET:", generate_state_token())
