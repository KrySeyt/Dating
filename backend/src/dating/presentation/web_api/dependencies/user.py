from fastapi import Body


def get_hashed_password(password: str = Body()) -> str:
    return str(hash(password))  # Just mock
