from cryptography.fernet import Fernet
import base64

def encrypt_data(data: str) -> str:
    return f"encrypted_{data}"

def decrypt_data(encrypted_data: str) -> str:
    return encrypted_data.replace("encrypted_", "")
