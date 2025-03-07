from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Configure a custom logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_extension")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response

# Define an extension class
class MyExtension:
    def __init__(self, app: FastAPI):
        self.app = app
        # Add the custom logging middleware
        self.app.add_middleware(LoggingMiddleware)

    def custom_error_handler(self, exc: HTTPException):
        logger.error(f"Error: {exc.detail}")
        return {"error": "Something went wrong!"}

    def setup(self):
        # Example of how you can add custom functionality here
        self.app.add_exception_handler(HTTPException, self.custom_error_handler)
