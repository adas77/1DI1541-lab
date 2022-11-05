import hashlib
import hmac
import os


def hash_new_password(password: str, salt: bytes) -> bytes:
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return pw_hash


def decode_password(salt: bytes, password: str):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)


def test_is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    return hmac.compare_digest(
        pw_hash,
        decode_password(salt, password)
    )


SALT = "random sól"
SALT = str.encode(SALT)

pw_hash = hash_new_password('correct horse battery staple', SALT)
assert test_is_correct_password(SALT, pw_hash, 'correct horse battery staple')
assert not test_is_correct_password(SALT, pw_hash, 'Tr0ub4dor&3')
assert not test_is_correct_password(SALT, pw_hash, 'rosebud')
