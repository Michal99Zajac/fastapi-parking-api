from fastapi import HTTPException, status


def not_found_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found",
    )


def forbidden_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail if detail else "Access to resources forbidden",
    )
