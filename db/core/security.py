from passlib.context import CryptContext
from datetime import datetime, UTC, timedelta
import jwt

from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Формат содержимого токена:
    {
        username: string, -> from data
        user_id: int, -> from data
        role: string, -> from data
        exp: float -> in func
    }
    """
    expire_time = timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)

    to_encode = data.copy()
    expire = datetime.now(UTC) + expire_time

    to_encode.update({"exp": expire.timestamp()})
    print(to_encode)

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)

if __name__ == "__main__":
    user = {
        "username": "test",
        "user_id": 123,
        "role": "admin",
    }
    print(create_access_token(data=user))

