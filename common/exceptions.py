from fastapi import HTTPException


def http_exception(status_code: int, detail: str):
    return HTTPException(status_code=status_code, detail=detail)
