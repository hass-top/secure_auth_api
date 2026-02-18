from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
from jose import jwt
from jose import JWTError

from app.models.config import Settings

settings = Settings()

class JWTVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
   
        if request.url.path in ["/auth/login", "/auth/register", "/docs", "/openapi.json", "/test"  ]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Authorization token missing"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                {"detail": "Token expired"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except JWTError:
            return JSONResponse(
                {"detail": "Invalid token"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        response = await call_next(request)
        return response
