from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from authx import exceptions


class _ErrorHandler:
    """Base Handler for FastAPI handling AuthX exceptions."""

    MSG_TokenError = "Token Error"
    MSG_MissingTokenError = "Missing JWT in request"
    MSG_MissingCSRFTokenError = None  # Use detailed exception message
    MSG_TokenTypeError = "Bad token type"
    MSG_RevokedTokenError = "Invalid token"
    MSG_TokenRequiredError = "Token required"
    MSG_FreshTokenRequiredError = "Fresh token required"
    MSG_AccessTokenRequiredError = "Access token required"
    MSG_RefreshTokenRequiredError = "Refresh token required"
    MSG_CSRFError = "CSRF double submit does not match"
    MSG_JWTDecodeError = "Invalid Token"
    MSG_InsufficientScopeError = None  # Use detailed exception message showing required vs provided scopes

    async def _rate_limit_handler(
        self,
        request: Request,
        exc: exceptions.RateLimitExceeded,
    ) -> JSONResponse:
        pass

    async def _error_handler(
        self,
        request: Request,
        exc: exceptions.AuthXException,
        status_code: int,
        message: Optional[str],
    ) -> JSONResponse:
        """Generate the async function to be decorated by `FastAPI.exception_handler` decorator.

        Args:
            request (Request): The request object.
            exc (exceptions.AuthXException): Exception object.
            status_code (int): HTTP status code.
            message (str): Default message.

        Returns:
            JSONResponse: The JSON response.
        """
        pass

    def _set_app_exception_handler(
        self,
        app: FastAPI,
        exception: type[exceptions.AuthXException],
        status_code: int,
        message: Optional[str],
    ) -> None:
        pass

    def handle_errors(self, app: FastAPI) -> None:
        """Add the `FastAPI.exception_handlers` relative to AuthX exceptions.

        Args:
            app (FastAPI): the FastAPI application to handle errors for
        """
        pass
