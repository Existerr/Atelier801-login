import re
import binascii
import hashlib
import base64

def regex(pattern):
    return re.compile(pattern)

def encrypt(password):
    CRYPT_VALUES = [-9, 25, -92, -37, -117, 18, 112, -95, -5, -108, 40, -83, -107, 73, -92, -102, 46, -52, 49, -118, -79, -56, -72, 63, -69, -98, -118, -22, 46, -16, -22, -111]
    HEX_CHARS = "0123456789abcdef"

    toHash_sha256 = hashlib.sha256(password.encode()).hexdigest()

    ShaKikooBytes = []
    for char in toHash_sha256:
        ShaKikooBytes.append(ord(char))

    for indice in range(0, len(CRYPT_VALUES)):
        ShaKikooBytes.append(int(CRYPT_VALUES[indice] + indice))
    
    ShaKikooHex = ""
    for byte in ShaKikooBytes:
        firstId = (byte >> 4) & 15
        secondId = byte & 15
        ShaKikooHex = ShaKikooHex + HEX_CHARS[firstId] + HEX_CHARS[secondId]

    ShaKikooHex_bin = binascii.unhexlify(ShaKikooHex)
    ShaKikooHex_sha256_bin = hashlib.sha256(ShaKikooHex_bin).digest()
    ShaKikooHex_sha256_b64 = base64.b64encode(ShaKikooHex_sha256_bin)

    return ShaKikooHex_sha256_b64.decode()
