from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.utils import logger


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in settings.EXCLUDE_PATHS:
            logger.debug(f"Skipping API key check for {request.url.path}")
            response = await call_next(request)
            return response

        if 'Authorization' not in request.headers:
            api_key = request.headers.get(settings.API_KEY)
            if api_key != settings.API_KEY_VALUE:
                error_response = JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API key"},
                )
                return error_response
        # else:
        #     authorization: str = request.headers.get('Authorization')
        #     if not authorization or not authorization.startswith('Bearer '):
        #         error_response = JSONResponse(
        #             status_code=401,
        #             content={"detail": "Missing or invalid Authorization header"},
        #         )
        #         return error_response

        response = await call_next(request)
        return response
