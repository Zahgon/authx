"""Main module for AuthX."""

import contextlib
from collections.abc import Awaitable, Coroutine
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    Union,
    overload,
)

from fastapi import Depends, Request, Response, WebSocket

from authx._internal._callback import _CallbackHandler
from authx._internal._error import _ErrorHandler
from authx._internal._ratelimit import RateLimiter
from authx._internal._scopes import has_required_scopes
from authx._internal._session import SessionInfo
from authx._internal._utils import get_uuid
from authx.config import AuthXConfig
from authx.core import _get_token_from_request
from authx.dependencies import AuthXDependency
from authx.exceptions import (
    AuthXException,
    InsufficientScopeError,
    JWTDecodeError,
    MissingTokenError,
    RevokedTokenError,
)
from authx.schema import RequestToken, TokenPayload, TokenResponse
from authx.types import (
    DateTimeExpression,
    StringOrSequence,
    T,
    TokenLocations,
    TokenType,
)


class AuthX(_CallbackHandler[T], _ErrorHandler):
    """The base class for AuthX.

    AuthX enables JWT management within a FastAPI application.
    Its main purpose is to provide a reusable & simple syntax to protect API
    with JSON Web Token authentication.

    Args:
        config (AuthXConfig, optional): Configuration instance to use. Defaults to AuthXConfig().
        model (Optional[T], optional): Model type hint. Defaults to dict[str, Any].

    Note:
        AuthX is a Generic python object.
        Its TypeVar is not mandatory but helps type hinting furing development

    """

    def __init__(self, config: AuthXConfig = AuthXConfig(), model: Optional[T] = None) -> None:
        """AuthX base object.

        Args:
            config (AuthXConfig, optional): Configuration instance to use. Defaults to AuthXConfig().
            model (Optional[T], optional): Model type hint. Defaults to dict[str, Any].
        """
        self.model: Union[T, dict[str, Any]] = model if model is not None else {}
        super().__init__(model=model)
        super(_CallbackHandler, self).__init__()
        self._config = config
        self._session_store: Optional[Any] = None

    def load_config(self, config: AuthXConfig) -> None:
        """Load and store the configuration for the authentication system.

        Sets the internal configuration object with the provided authentication configuration.

        Args:
            config: The configuration settings for the AuthX authentication system.

        Returns:
            None
        """
        pass

    @property
    def config(self) -> AuthXConfig:
        """AuthX Configuration getter.

        Returns:
            AuthXConfig: Configuration BaseSettings
        """
        pass

    def _create_payload(
        self,
        uid: str,
        type: str,
        fresh: bool = False,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[dict[str, Any]] = None,
        audience: Optional[StringOrSequence] = None,
        scopes: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> TokenPayload:
        # Handle additional data
        pass

    def _create_token(
        self,
        uid: str,
        type: str,
        fresh: bool = False,
        headers: Optional[dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[dict[str, Any]] = None,
        audience: Optional[StringOrSequence] = None,
        scopes: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str:
        pass

    def _decode_token(
        self,
        token: str,
        verify: bool = True,
        audience: Optional[StringOrSequence] = None,
        issuer: Optional[str] = None,
    ) -> TokenPayload:
        pass

    def _set_cookies(
        self,
        token: str,
        type: str,
        response: Response,
        max_age: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        pass

    def _unset_cookies(
        self,
        type: str,
        response: Response,
    ) -> None:
        pass

    @overload
    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: Literal[False] = False,
    ) -> RequestToken: ...

    @overload
    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: Literal[True] = True,
    ) -> Optional[RequestToken]: ...

    async def _get_token_from_request(
        self,
        request: Request,
        locations: Optional[TokenLocations] = None,
        refresh: bool = False,
        optional: bool = False,
    ) -> Optional[RequestToken]:
        # Use configured token locations if not explicitly provided
        pass

    async def get_access_token_from_request(
        self, request: Request, locations: Optional[TokenLocations] = None
    ) -> RequestToken:
        """Dependency to retrieve access token from request.

        Args:
            request (Request): Request to retrieve access token from
            locations (Optional[TokenLocations], optional): Locations to retrieve token from. Defaults to None.

        Raises:
            MissingTokenError: When no `access` token is available in request

        Returns:
            RequestToken: Request Token instance for `access` token type
        """
        pass

    async def get_refresh_token_from_request(
        self, request: Request, locations: Optional[TokenLocations] = None
    ) -> RequestToken:
        """Dependency to retrieve refresh token from request.

        Args:
            request (Request): Request to retrieve refresh token from
            locations (Optional[TokenLocations], optional): Locations to retrieve token from. Defaults to None.

        Raises:
            MissingTokenError: When no `refresh` token is available in request

        Returns:
            RequestToken: Request Token instance for `refresh` token type
        """
        pass

    async def _auth_required(
        self,
        request: Request,
        type: str = "access",
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
        locations: Optional[TokenLocations] = None,
    ) -> TokenPayload:
        pass

    def verify_token(
        self,
        token: RequestToken,
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: bool = True,
    ) -> TokenPayload:
        """Verify a request token.

        Attempts verification with the current key first, then falls back
        to the previous key if key rotation is configured.

        Args:
            token (RequestToken): RequestToken instance
            verify_type (bool, optional): Apply token type verification. Defaults to True.
            verify_fresh (bool, optional): Apply token freshness verification. Defaults to False.
            verify_csrf (bool, optional): Apply token CSRF verification. Defaults to True.

        Returns:
            TokenPayload: Verified token payload
        """
        pass

    def create_access_token(
        self,
        uid: str,
        fresh: bool = False,
        headers: Optional[dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[dict[str, Any]] = None,
        audience: Optional[StringOrSequence] = None,
        scopes: Optional[list[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Generate an Access Token.

        Args:
            uid (str): Unique identifier to generate token for
            fresh (bool, optional): Generate fresh token. Defaults to False.
            headers (Optional[dict[str, Any]], optional): Custom JWT headers. Defaults to None.
            expiry (Optional[DateTimeExpression], optional): Use a user defined expiry claim. Defaults to None.
            data (Optional[dict[str, Any]], optional): Additional data to store in token. Defaults to None.
            audience (Optional[StringOrSequence], optional): Audience claim. Defaults to None.
            scopes (Optional[list[str]], optional): List of scopes to include in the token. Defaults to None.

        Returns:
            str: Access Token

        Example:
            ```python
            # Token with scopes
            token = auth.create_access_token(
                uid="user123",
                scopes=["users:read", "posts:write"]
            )
            ```
        """
        pass

    def create_refresh_token(
        self,
        uid: str,
        headers: Optional[dict[str, Any]] = None,
        expiry: Optional[DateTimeExpression] = None,
        data: Optional[dict[str, Any]] = None,
        audience: Optional[StringOrSequence] = None,
        scopes: Optional[list[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Generate a Refresh Token.

        Args:
            uid (str): Unique identifier to generate token for
            headers (Optional[dict[str, Any]], optional): Custom JWT headers. Defaults to None.
            expiry (Optional[DateTimeExpression], optional): Use a user defined expiry claim. Defaults to None.
            data (Optional[dict[str, Any]], optional): Additional data to store in token. Defaults to None.
            audience (Optional[StringOrSequence], optional): Audience claim. Defaults to None.
            scopes (Optional[list[str]], optional): List of scopes to include in the token. Defaults to None.

        Returns:
            str: Refresh Token
        """
        pass

    def create_token_pair(
        self,
        uid: str,
        fresh: bool = False,
        headers: Optional[dict[str, Any]] = None,
        access_expiry: Optional[DateTimeExpression] = None,
        refresh_expiry: Optional[DateTimeExpression] = None,
        data: Optional[dict[str, Any]] = None,
        audience: Optional[StringOrSequence] = None,
        access_scopes: Optional[list[str]] = None,
        refresh_scopes: Optional[list[str]] = None,
    ) -> TokenResponse:
        """Generate an access and refresh token pair.

        Convenience method that creates both tokens at once and returns them
        in a standardized ``TokenResponse`` model.

        Args:
            uid: Unique identifier of the user.
            fresh: Whether the access token should be marked as fresh. Defaults to False.
            headers: Optional custom JWT headers applied to both tokens.
            access_expiry: Optional expiry override for the access token.
            refresh_expiry: Optional expiry override for the refresh token.
            data: Optional additional data stored in both tokens.
            audience: Optional audience claim for both tokens.
            access_scopes: Optional scopes for the access token.
            refresh_scopes: Optional scopes for the refresh token.

        Returns:
            TokenResponse: A model containing ``access_token``, ``refresh_token``, and ``token_type``.

        Example:
            ```python
            tokens = auth.create_token_pair(uid="user123", fresh=True)
            return tokens  # {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
            ```
        """
        pass

    def set_access_cookies(
        self,
        token: str,
        response: Response,
        max_age: Optional[int] = None,
    ) -> None:
        """Add 'Set-Cookie' for access token in response header.

        Args:
            token (str): Access token
            response (Response): response to set cookie on
            max_age (Optional[int], optional): Max Age cookie parameter. Defaults to None.
        """
        pass

    def set_refresh_cookies(
        self,
        token: str,
        response: Response,
        max_age: Optional[int] = None,
    ) -> None:
        """Add 'Set-Cookie' for refresh token in response header.

        Args:
            token (str): Refresh token
            response (Response): response to set cookie on
            max_age (Optional[int], optional): Max Age cookie parameter. Defaults to None.
        """
        pass

    def unset_access_cookies(
        self,
        response: Response,
    ) -> None:
        """Remove 'Set-Cookie' for access token in response header.

        Args:
            response (Response): response to remove cooke from
        """
        pass

    def unset_refresh_cookies(
        self,
        response: Response,
    ) -> None:
        """Remove 'Set-Cookie' for refresh token in response header.

        Args:
            response (Response): response to remove cooke from
        """
        pass

    def unset_cookies(
        self,
        response: Response,
    ) -> None:
        """Remove 'Set-Cookie' for tokens from response headers.

        Args:
            response (Response): response to remove token cookies from
        """
        pass

    # Notes:
    # The AuthXDeps is a utility class, to enable quick token operations
    # within the route logic. It provides methods to avoid additional code
    # in your route that would be outside of the route logic

    # Such methods includes setting and unsetting cookies without the need
    # to generate a response object beforehand.

    @property
    def DEPENDENCY(self) -> AuthXDependency[Any]:
        """FastAPI Dependency to return an AuthX sub-object within the route context."""
        pass

    @property
    def BUNDLE(self) -> AuthXDependency[Any]:
        """FastAPI Dependency to return a AuthX sub-object within the route context."""
        pass

    @property
    def FRESH_REQUIRED(self) -> TokenPayload:
        """FastAPI Dependency to enforce valid token availability in request."""
        pass

    @property
    def ACCESS_REQUIRED(self) -> TokenPayload:
        """FastAPI Dependency to enforce presence of an `access` token in request."""
        pass

    @property
    def REFRESH_REQUIRED(self) -> TokenPayload:
        """FastAPI Dependency to enforce presence of a `refresh` token in request."""
        pass

    @property
    def ACCESS_TOKEN(self) -> RequestToken:
        """FastAPI Dependency to retrieve access token from request."""
        pass

    @property
    def REFRESH_TOKEN(self) -> RequestToken:
        """FastAPI Dependency to retrieve refresh token from request."""
        pass

    @property
    def CURRENT_SUBJECT(self) -> T:
        """FastAPI Dependency to retrieve the current subject from request."""
        pass

    @property
    def WS_AUTH_REQUIRED(self) -> TokenPayload:
        """FastAPI Dependency to enforce valid access token on a WebSocket connection.

        Extracts the token from the ``token`` query parameter or the ``Authorization``
        header of the WebSocket handshake request.
        """
        pass

    async def _ws_auth_required(self, websocket: WebSocket) -> TokenPayload:
        """Verify an access token from a WebSocket connection.

        Looks for the token in the query string (``?token=...``) first,
        then falls back to the ``Authorization`` header.

        Raises:
            MissingTokenError: When no token is found.
            JWTDecodeError: When the token is invalid.
        """
        pass

    def get_dependency(self, request: Request, response: Response) -> AuthXDependency[Any]:
        """FastAPI Dependency to return a AuthX sub-object within the route context.

        Args:
            request (Request): Request context managed by FastAPI
            response (Response): Response context managed by FastAPI

        Note:
            The AuthXDeps is a utility class, to enable quick token operations
            within the route logic. It provides methods to avoid additional code
            in your route that would be outside of the route logic

            Such methods includes setting and unsetting cookies without the need
            to generate a response object beforehand

        Returns:
            AuthXDeps: The contextful AuthX object
        """
        pass

    def token_required(
        self,
        type: str = "access",
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
        locations: Optional[TokenLocations] = None,
    ) -> Callable[[Request], Awaitable[TokenPayload]]:
        """Dependency to enforce valid token availability in request.

        Args:
            type (str, optional): Require a given token type. Defaults to "access".
            verify_type (bool, optional): Apply type verification. Defaults to True.
            verify_fresh (bool, optional): Require token freshness. Defaults to False.
            verify_csrf (Optional[bool], optional): Enable CSRF verification. Defaults to None.
            locations (Optional[TokenLocations], optional): Locations to retrieve token from. Defaults to None.

        Returns:
            Callable[[Request], TokenPayload]: Dependency for Valid token Payload retrieval
        """
        pass

    @property
    def fresh_token_required(self) -> Callable[[Request], Awaitable[TokenPayload]]:
        """FastAPI Dependency to enforce presence of a `fresh` `access` token in request."""
        pass

    @property
    def access_token_required(self) -> Callable[[Request], Awaitable[TokenPayload]]:
        """FastAPI Dependency to enforce presence of an `access` token in request."""
        pass

    @property
    def refresh_token_required(self) -> Callable[[Request], Awaitable[TokenPayload]]:
        """FastAPI Dependency to enforce presence of a `refresh` token in request."""
        pass

    def scopes_required(
        self,
        *scopes: str,
        all_required: bool = True,
        verify_type: bool = True,
        verify_fresh: bool = False,
        verify_csrf: Optional[bool] = None,
        locations: Optional[TokenLocations] = None,
    ) -> Callable[[Request], Awaitable[TokenPayload]]:
        """Dependency to enforce required scopes in token.

        Creates a FastAPI dependency that validates that the token contains
        the required scopes. Supports both simple and hierarchical scopes
        with wildcard matching (e.g., "admin:*" matches "admin:users").

        Args:
            *scopes: Variable number of scope strings required.
            all_required: If True (default), ALL scopes must be present (AND logic).
                         If False, at least ONE scope must be present (OR logic).
            verify_type: Apply token type verification. Defaults to True.
            verify_fresh: Require token freshness. Defaults to False.
            verify_csrf: Enable CSRF verification. Defaults to None (uses config).
            locations: Locations to retrieve token from. Defaults to None.

        Returns:
            Callable[[Request], Awaitable[TokenPayload]]: Dependency for scope validation.

        Raises:
            InsufficientScopeError: When token lacks required scopes.

        Example:
            ```python
            # Require single scope
            @app.get("/users", dependencies=[Depends(auth.scopes_required("users:read"))])
            async def list_users(): ...

            # Require multiple scopes (AND)
            @app.delete("/users/{id}", dependencies=[Depends(auth.scopes_required("users:read", "users:delete"))])
            async def delete_user(id: int): ...

            # Require any of the scopes (OR)
            @app.get("/admin", dependencies=[Depends(auth.scopes_required("admin", "superuser", all_required=False))])
            async def admin_panel(): ...

            # Wildcard scope
            @app.get("/admin/users", dependencies=[Depends(auth.scopes_required("admin:*"))])
            async def admin_users(): ...
            ```
        """
        pass

    async def get_current_subject(self, request: Request) -> Optional[T]:
        """Retrieve the currently authenticated subject from the request.

        Validates the request token and fetches the corresponding subject based on the user identifier.

        Args:
            request: The HTTP request containing authentication credentials.

        Returns:
            The authenticated subject if present, otherwise None.
        """
        pass

    @overload
    async def get_token_from_request(
        self,
        request: Request,
        type: TokenType = "access",
        optional: Literal[True] = True,
        locations: Optional[TokenLocations] = None,
    ) -> Optional[RequestToken]: ...

    @overload
    async def get_token_from_request(
        self,
        request: Request,
        type: TokenType = "access",
        optional: Literal[False] = False,
        locations: Optional[TokenLocations] = None,
    ) -> RequestToken: ...

    async def get_token_from_request(
        self,
        request: Request,
        type: TokenType = "access",
        optional: bool = True,
        locations: Optional[TokenLocations] = None,
    ) -> Optional[RequestToken]:
        """Retrieve token from request.

        Args:
            request (Request): The FastAPI request object.
            type (TokenType, optional): The type of token to retrieve from request.
                Defaults to "access".
            optional (bool, optional): Whether or not to enforce token presence in request.
                Defaults to True.
            locations (Optional[TokenLocations], optional): Locations to retrieve token from.
                Defaults to None (uses configured JWT_TOKEN_LOCATION).

        Note:
            When `optional=True`, the return value might be `None`
            if no token is available in request.

            When `optional=False`, raises a MissingTokenError.

        Returns:
            Optional[RequestToken]: The RequestToken if available, None if optional and not found.

        Example:
            ```python
            token = await auth.get_token_from_request(request)
            token = await auth.get_token_from_request(request, type="refresh")
            token = await auth.get_token_from_request(request, optional=False)
            ```
        """
        pass

    def _implicit_refresh_enabled_for_request(self, request: Request) -> bool:
        """Check if a request should implement implicit token refresh.

        Args:
            request (Request): Request to check

        Returns:
            bool: True if request allows for refreshing access token
        """
        pass

    async def implicit_refresh_middleware(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        """FastAPI Middleware to enable token refresh for an APIRouter.

        Args:
            request (Request): Incoming request
            call_next (Coroutine): Endpoint logic to be called

        Note:
            This middleware is only based on `access` tokens.
            Using implicit refresh mechanism makes use of `refresh`
            tokens unnecessary.

        Note:
            The refreshed `access` token will not be considered as
            `fresh`

        Note:
            The implicit refresh mechanism is only enabled
            for authorization through cookies.

        Returns:
            Response: Response with update access token cookie if relevant
        """
        pass

    def rate_limited(
        self,
        max_requests: int = 10,
        window: int = 60,
        key_func: Optional[Callable[[Request], str]] = None,
    ) -> Callable[[Request], Awaitable[TokenPayload]]:
        """Dependency combining rate limiting with access token verification.

        Args:
            max_requests: Maximum requests allowed within the window.
            window: Time window in seconds.
            key_func: Callable to extract rate limit key from request. Defaults to client IP.

        Returns:
            A FastAPI dependency that enforces both rate limiting and token auth.

        Example:
            ```python
            @app.get("/api", dependencies=[Depends(auth.rate_limited(max_requests=5, window=60))])
            async def api_route(): ...
            ```
        """
        pass

    # --- Session Management ---

    def set_session_store(self, store: Any) -> None:
        """Register a session storage backend.

        Args:
            store: An object implementing the ``SessionStoreProtocol``.
        """
        pass

    async def create_session(
        self,
        uid: str,
        request: Optional[Request] = None,
        device_info: Optional[dict[str, Any]] = None,
    ) -> SessionInfo:
        """Create a new session and persist it via the session store.

        Args:
            uid: User identifier.
            request: Optional HTTP request for IP/User-Agent extraction.
            device_info: Optional additional device metadata.

        Returns:
            The created ``SessionInfo`` instance.
        """
        pass

    async def list_sessions(self, uid: str) -> list[SessionInfo]:
        """List all active sessions for a user.

        Args:
            uid: User identifier.

        Returns:
            List of active ``SessionInfo`` objects.
        """
        pass

    async def revoke_session(self, session_id: str) -> None:
        """Revoke a single session by ID.

        Args:
            session_id: The session to revoke.
        """
        pass

    async def revoke_all_sessions(self, uid: str) -> None:
        """Revoke all sessions for a user.

        Args:
            uid: User identifier.
        """
        pass

    async def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Retrieve a session by ID.

        Args:
            session_id: The session to look up.

        Returns:
            The ``SessionInfo`` if found and active, otherwise None.
        """
        pass
