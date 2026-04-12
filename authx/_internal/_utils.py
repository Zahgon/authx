import datetime as dt
import uuid
from datetime import datetime, timedelta
from datetime import timezone as tz
from typing import Union

from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
from pytz import BaseTzInfo, timezone

from authx.types import Numeric

RESERVED_CLAIMS = {
    "fresh",
    "csrf",
    "iat",
    "exp",
    "iss",
    "aud",
    "type",
    "jti",
    "nbf",
    "sub",
}

utc = timezone("UTC")


def get_now() -> dt.datetime:
    return dt.datetime.now(tz=dt.timezone.utc)


def get_now_ts() -> Numeric:
    return get_now().timestamp()


def get_uuid() -> str:
    return str(uuid.uuid4())


def time_diff(dt1: datetime, dt2: datetime) -> relativedelta:
    pass


def to_UTC(event_timestamp: Union[datetime, str], tz: BaseTzInfo = utc) -> datetime:
    pass


def to_UTC_without_tz(event_timestamp: str, format: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    pass


def beginning_of_day(dt: datetime) -> datetime:
    pass


def end_of_day(dt: datetime) -> datetime:
    pass


def minutes_ago(dt: datetime, days: int = 0, hours: int = 0, minutes: int = 1, seconds: int = 0) -> datetime:
    pass


def minutes_after(dt: datetime, days: int = 0, hours: int = 0, minutes: int = 1, seconds: int = 0) -> datetime:
    pass


def hours_ago(dt: datetime, days: int = 0, hours: int = 1, minutes: int = 0, seconds: int = 0) -> datetime:
    pass


def days_ago(dt: datetime, days: int = 1, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
    pass


def months_ago(dt: datetime, months: int = 1) -> datetime:
    pass


def months_after(dt: datetime, months: int = 1) -> datetime:
    pass


def years_ago(dt: datetime, years: int = 1) -> datetime:
    pass


def days_after(dt: datetime, days: int = 1, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
    pass


def is_today(dt: datetime) -> bool:
    pass


def is_yesterday(dt: datetime) -> bool:
    pass


def is_tomorrow(dt: datetime) -> bool:
    pass


def IST_time() -> datetime:
    pass


def tz_now(tz: BaseTzInfo = utc) -> datetime:
    pass


def tz_from_iso(dt: str, to_tz: BaseTzInfo = utc, format: str = "%Y-%m-%dT%H:%M:%S.%f%z") -> datetime:
    pass


def start_of_week(dt: Union[str, datetime], to_tz: BaseTzInfo = utc) -> datetime:
    pass


def end_of_week(dt: Union[str, datetime], to_tz: BaseTzInfo = utc) -> datetime:
    pass


def end_of_last_week(dt: Union[str, datetime], to_tz: BaseTzInfo = utc) -> datetime:
    pass
