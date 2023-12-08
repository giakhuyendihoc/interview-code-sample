import datetime
from typing import TypedDict

import jwt

from main import config

ALGORITHM = "HS256"


class JWTPayload(TypedDict):
    sub: int
    iat: datetime.datetime
    exp: datetime.datetime


def encode(
    user_id: int,
    lifetime=config.JWT_LIFETIME_IN_SECONDS,
) -> str:
    iat = datetime.datetime.utcnow()
    payload: JWTPayload = {
        "sub": user_id,
        "iat": iat,
        "exp": iat + datetime.timedelta(seconds=lifetime),
    }

    return jwt.encode(
        payload,
        config.JWT_SECRET,
        algorithm=ALGORITHM,
    )


def decode(access_token: str) -> JWTPayload:
    token = jwt.decode(
        access_token,
        config.JWT_SECRET,
        leeway=10,
        algorithms=[ALGORITHM],
    )
    return token
