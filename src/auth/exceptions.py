from fastapi import HTTPException, status


def unauthhorized_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def invalid_credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User doesn't have required permissions",
    )


def invalid_password_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid password",
    )
