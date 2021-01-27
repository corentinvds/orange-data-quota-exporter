# coding=utf-8
from datetime import datetime

import pytz
from pytz import UTC

__TZ = pytz.timezone('Europe/Brussels')


def localized_now():
    return localize(UTC.localize(datetime.utcnow()))


def localize(dt: datetime):
    if dt.tzinfo is not None:
        return dt.astimezone(__TZ)
    else:
        return __TZ.localize(dt)
