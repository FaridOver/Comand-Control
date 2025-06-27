from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256

password = b"clave_admin_123"
salt = b"target_01"
key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)

def payload_encrypt(mensaje: bytes): #mensaje en binario
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(mensaje)
    return nonce + tag + ciphertext #encriptado en binario hexadecimal

