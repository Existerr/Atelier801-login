import re
import hashlib
import base64

SALT = bytes((
	0xf7, 0x1a, 0xa6, 0xde, 0x8f, 0x17, 0x76, 0xa8, 0x03, 0x9d, 0x32, 0xb8, 0xa1, 0x56, 0xb2, 0xa9,
	0x3e, 0xdd, 0x43, 0x9d, 0xc5, 0xdd, 0xce, 0x56, 0xd3, 0xb7, 0xa4, 0x05, 0x4a, 0x0d, 0x08, 0xb0
))

def regex(pattern):
    return re.compile(pattern)

def encrypt(string):
	sha256 = hashlib.sha256(string.encode())
	hex256 = sha256.hexdigest().encode()
	hex256 += SALT

	hashed = hashlib.sha256(hex256).digest()
	return base64.b64encode(hashed).decode()
