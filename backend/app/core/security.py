from passlib.context import CryptContext
pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(p):
    return pwd_ctx.hash(p)

def verify_password(p, h):
    return pwd_ctx.verify(p, h)
