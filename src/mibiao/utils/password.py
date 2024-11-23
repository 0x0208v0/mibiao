from passlib.context import CryptContext

# 用 werkzeug 的 check_password_hash 会突然增加30MB内存占用？？
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password_hash(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)
