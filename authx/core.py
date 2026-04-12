"""Core functions for AuthX."""

import contextlib
from typing import Any, Literal, Optional

from fastapi import Request

from authx.config import AuthXConfig
from authx.exceptions import CSRFError, MissingCSRFTokenError, MissingTokenError
from authx.schema import RequestToken
from authx.types import TokenLocations


async def _get_token_from_headers(
    request: Request, config: AuthXConfig, refresh: bool = False, **kwargs: Any
) -> RequestToken:
    """Get access token from headers."""
    pass


async def _get_token_from_cookies(
    request: Request, config: AuthXConfig, refresh: bool = False, **kwargs: Any
) -> RequestToken:
    """Get access token from cookies.

    Args:
        request (Request): FastAPI Request
        config (AuthXConfig): AuthX Configuration
        refresh (bool, optional): If True, get refresh token. Defaults to False.

    Raises:
        MissingTokenError: If cookie is not set
        MissingCSRFTokenError: If CSRF token is not set

    Returns:
        RequestToken: RequestToken instance
    """
    pass


async def _get_token_from_query(
    request: Request, config: AuthXConfig, refresh: bool = False, **kwargs: Any
) -> RequestToken:
    pass


async def _get_token_from_json(
    request: Request, config: AuthXConfig, refresh: bool = False, **kwargs: Any
) -> RequestToken:
    pass


TOKEN_GETTERS = {
    "json": _get_token_from_json,
    "query": _get_token_from_query,
    "cookies": _get_token_from_cookies,
    "headers": _get_token_from_headers,
}


async def _get_token_from_request(
    request: Request,
    config: AuthXConfig,
    refresh: bool = False,
    locations: Optional[TokenLocations] = None,
    **kwargs: Any,
) -> RequestToken:
    pass
