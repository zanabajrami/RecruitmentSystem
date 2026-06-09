from fastapi import HTTPException, status

class CustomAPIException(HTTPException):
    def __init__(self, status_code: int, detail: str, code: str = "BAD_REQUEST"):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code

class NotFoundException(CustomAPIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, code="NOT_FOUND")

class BadRequestException(CustomAPIException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, code="BAD_REQUEST")

class UnauthorizedException(CustomAPIException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, code="UNAUTHORIZED")