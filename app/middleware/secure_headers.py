from  starlette.middleware.base import BaseHTTPMiddleware 
from  starlette.responses import Response 

class SecureHeaderMiddleware ( BaseHTTPMiddleware ) : 
    async def dispatch(self, request, call_next):
        response: Response = await call_next ( request ) 
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=()'
        return response 
    