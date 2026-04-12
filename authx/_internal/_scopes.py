"""Scope management utilities for AuthX.

This module provides functions for matching and validating scopes with support for:
- Simple string scopes (e.g., "read", "write", "admin")
- Hierarchical scopes with colon separator (e.g., "users:read", "posts:write")
- Wildcard patterns (e.g., "admin:*" matches "admin:users", "admin:settings")
"""

from collections.abc import Sequence
from typing import Optional


def match_scope(required: str, provided: str) -> bool:
    """Check if a provided scope matches a required scope.

    Supports wildcard matching where a scope ending with ":*" matches
    any scope under that namespace.

    Args:
        required: The scope that is required (e.g., "users:read").
        provided: The scope that was provided in the token (e.g., "users:*").

    Returns:
        True if the provided scope satisfies the required scope.

    Examples:
        >>> match_scope("read", "read")
        True
        >>> match_scope("users:read", "users:*")
        True
        >>> match_scope("users:read", "admin:*")
        False
        >>> match_scope("admin", "admin:*")
        True
        >>> match_scope("admin:users:edit", "admin:*")
        True
    """
    pass


def has_required_scopes(
    required: Sequence[str],
    provided: Optional[Sequence[str]],
    all_required: bool = True,
) -> bool:
    """Check if the provided scopes satisfy the required scopes.

    Args:
        required: List of scopes that are required.
        provided: List of scopes that were provided in the token.
        all_required: If True, all required scopes must be satisfied (AND logic).
                      If False, at least one required scope must be satisfied (OR logic).

    Returns:
        True if the scope requirements are satisfied.

    Examples:
        >>> has_required_scopes(["read"], ["read", "write"], all_required=True)
        True
        >>> has_required_scopes(["read", "admin"], ["read"], all_required=True)
        False
        >>> has_required_scopes(["read", "admin"], ["read"], all_required=False)
        True
        >>> has_required_scopes(["users:read"], ["users:*"], all_required=True)
        True
    """
    pass


def normalize_scope(scope: str) -> str:
    """Normalize a scope string by stripping whitespace and converting to lowercase.

    Args:
        scope: The scope string to normalize.

    Returns:
        The normalized scope string.
    """
    pass


def parse_scope_string(scope_string: str, delimiter: str = " ") -> list[str]:
    """Parse a space-separated scope string into a list of scopes.

    This is useful for OAuth2 compatibility where scopes are often passed
    as a single space-separated string.

    Args:
        scope_string: A string containing scopes separated by the delimiter.
        delimiter: The delimiter used to separate scopes. Defaults to space.

    Returns:
        A list of individual scope strings.

    Examples:
        >>> parse_scope_string("read write admin")
        ["read", "write", "admin"]
        >>> parse_scope_string("users:read users:write")
        ["users:read", "users:write"]
    """
    pass
