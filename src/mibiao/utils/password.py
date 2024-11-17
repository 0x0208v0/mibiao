from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password_hash(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)
