import bcrypt


def generate_hashed_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        salt=bcrypt.gensalt(),
    ).decode("utf-8")


def is_valid_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
