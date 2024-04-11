# app/main.py
from fastapi import FastAPI
from starlette.middleware.errors import ServerErrorMiddleware
from app.core.middleware import APIKeyMiddleware
from app.api.api_v1.endpoints import users, items, status
from app.core import authentication
from app.core.config import settings


app = FastAPI(debug=settings.DEBUG,
              title=settings.PROJECT_NAME,
              version=settings.VERSION,
              openapi_url=settings.OPENAPI_URL,
              docs_url=settings.DOCS_URL,
              redoc_url=settings.REDOC_URL)

# Add built-in middleware
# app.add_middleware(ServerErrorMiddleware)
# app.include_router(authentication.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(status.router, prefix="/api/v1/status", tags=["status"])

# Add your custom middleware last
app.add_middleware(APIKeyMiddleware)
