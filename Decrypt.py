from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import AES

# Usar la misma clave derivada en el cifrado
password = b"clave_admin_123"
salt = b"target_01"
key = PBKDF2(password, salt, dkLen=16, count=100_000, hmac_hash_module=SHA256)

def payload_decrypt(ciphertext_with_nonce_and_tag): #cipher... en binario hexadecimal
    # Extraer nonce, tag y ciphertext de los datos cifrados
    nonce = ciphertext_with_nonce_and_tag[:12]
    tag = ciphertext_with_nonce_and_tag[12:28]
    ciphertext = ciphertext_with_nonce_and_tag[28:]

    # Inicializar el descifrador AES en modo GCM
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Realizar el descifrado y verificar la integridad con el tag
    try:
        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_message
    except ValueError:
        raise ValueError("El mensaje ha sido alterado o el tag de autenticación es incorrecto.")


