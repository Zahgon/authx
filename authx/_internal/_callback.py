import sys
from inspect import iscoroutinefunction

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpecKwargs
else:
    from typing_extensions import ParamSpecKwargs  # pragma: no cover

from typing import Generic, Optional, cast

from authx.types import ModelCallback, T, TokenCallback


class _CallbackHandler(Generic[T]):
    """Base class for callback handlers in AuthX.

    Args:
        Generic (T): Model type

    Raises:
        AttributeError: If callback is not set
    """

    def __init__(self, model: Optional[T] = None) -> None:
        """Base class for callback handlers in AuthX.

        Args:
            model (T): Model instance
        """
        self._model: Optional[T] = model
        self.callback_get_model_instance: Optional[ModelCallback[T]] = None
        self.callback_is_token_in_blocklist: Optional[TokenCallback] = None

        # Exceptions
        self._callback_model_set_exception = AttributeError(
            f"Model callback not set for {self._model.__class__.__name__} instance"
        )
        self._callback_token_set_exception = AttributeError(
            f"Token callback not set for {self._model.__class__.__name__} instance"
        )

    @property
    def is_model_callback_set(self) -> bool:
        """Check if callback is set for model instance."""
        pass

    @property
    def is_token_callback_set(self) -> bool:
        """Check if callback is set for token."""
        pass

    def _check_model_callback_is_set(self, ignore_errors: bool = False) -> bool:
        """Check if callback is set for model instance and raise exception if not set."""
        pass

    def _check_token_callback_is_set(self, ignore_errors: bool = False) -> bool:
        """Check if callback is set for token and raise exception if not set."""
        pass

    def set_callback_get_model_instance(self, callback: ModelCallback[T]) -> None:
        """Set callback for model instance."""
        pass

    def set_callback_token_blocklist(self, callback: TokenCallback) -> None:
        """Set callback for token."""
        pass

    def set_subject_getter(self, callback: ModelCallback[T]) -> None:
        """Set the callback to run for subject retrieval and serialization."""
        pass

    def set_token_blocklist(self, callback: TokenCallback) -> None:
        """Set the callback to run for validation of revoked tokens."""
        pass

    async def _get_current_subject(self, uid: str, **kwargs: ParamSpecKwargs) -> Optional[T]:
        """Get current model instance from callback."""
        pass

    async def is_token_in_blocklist(self, token: Optional[str], **kwargs: ParamSpecKwargs) -> bool:
        """Check if token is in blocklist."""
        pass
