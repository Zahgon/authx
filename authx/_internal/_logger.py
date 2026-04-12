import logging
import sys
import traceback
from typing import Optional

log = logging.getLogger("authx")


def get_logger() -> logging.Logger:
    pass


def set_log_level(level: str) -> logging.Logger:
    pass


def log_debug(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> None:
    pass


def log_info(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> None:
    pass


def log_error(
    msg: str,
    loc: Optional[str] = None,
    method: Optional[str] = None,
    e: Optional[Exception] = None,
) -> None:
    pass


def _build_log_msg(msg: str, loc: Optional[str] = None, method: Optional[str] = None) -> str:
    pass


logging.basicConfig()
logging.StreamHandler(sys.stdout)
log.setLevel(logging.DEBUG)
