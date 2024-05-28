from fastapi import FastAPI
from routes.no_auth_routes import no_auth_router
from routes.auth_routes import auth_router
from routes.admin_routes import admin_router
from middleware.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(no_auth_router)


