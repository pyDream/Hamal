
"""
Time related utilities and helper functions.
"""

import calendar
import datetime
import time

import six


# ISO 8601 extended time format with microseconds
_ISO8601_TIME_FORMAT_SUBSECOND = '%Y-%m-%dT%H:%M:%S.%f'
_ISO8601_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
PERFECT_TIME_FORMAT = _ISO8601_TIME_FORMAT_SUBSECOND


def isotime(at=None, subsecond=False):
    """Stringify time in ISO 8601 format."""
    if not at:
        at = utcnow()
    st = at.strftime(_ISO8601_TIME_FORMAT
                     if not subsecond
                     else _ISO8601_TIME_FORMAT_SUBSECOND)
    try:
        tz = at.tzinfo.tzname(None) if at.tzinfo else 'UTC'
    except AttributeError:
        tz = 'UTC'
    st += ('Z' if tz == 'UTC' else tz)
    return st

def strtime(at=None, fmt=PERFECT_TIME_FORMAT):
    """Returns formatted utcnow."""
    if not at:
        at = utcnow()
    return at.strftime(fmt)


def parse_strtime(timestr, fmt=PERFECT_TIME_FORMAT):
    """Turn a formatted time back into a datetime."""
    return datetime.datetime.strptime(timestr, fmt)


def normalize_time(timestamp):
    """Normalize time in arbitrary timezone to UTC naive object."""
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset


def is_older_than(before, seconds):
    """Return True if before is older than seconds."""
    if isinstance(before, six.string_types):
        before = parse_strtime(before).replace(tzinfo=None)
    return utcnow() - before > datetime.timedelta(seconds=seconds)


def is_newer_than(after, seconds):
    """Return True if after is newer than seconds."""
    if isinstance(after, six.string_types):
        after = parse_strtime(after).replace(tzinfo=None)
    return after - utcnow() > datetime.timedelta(seconds=seconds)


def utcnow_ts():
    """Timestamp version of our utcnow function."""
    if utcnow.override_time is None:
        # NOTE(kgriffs): This is several times faster
        # than going through calendar.timegm(...)
        return int(time.time())

    return calendar.timegm(utcnow().timetuple())


def utcnow():
    """Overridable version of utils.utcnow."""
    if utcnow.override_time:
        try:
            return utcnow.override_time.pop(0)
        except AttributeError:
            return utcnow.override_time
    return datetime.datetime.utcnow()

utcnow.override_time = None


def set_time_override(override_time=None):
    """Overrides utils.utcnow.

    Make it return a constant time or a list thereof, one at a time.

    :param override_time: datetime instance or list thereof. If not
                          given, defaults to the current UTC time.
    """
    utcnow.override_time = override_time or datetime.datetime.utcnow()


def advance_time_delta(timedelta):
    """Advance overridden time using a datetime.timedelta."""
    assert(not utcnow.override_time is None)
    try:
        for dt in utcnow.override_time:
            dt += timedelta
    except TypeError:
        utcnow.override_time += timedelta


def advance_time_seconds(seconds):
    """Advance overridden time by seconds."""
    advance_time_delta(datetime.timedelta(0, seconds))


def clear_time_override():
    """Remove the overridden time."""
    utcnow.override_time = None


def marshall_now(now=None):
    """Make an rpc-safe datetime with microseconds.

    Note: tzinfo is stripped, but not required for relative times.
    """
    if not now:
        now = utcnow()
    return dict(day=now.day, month=now.month, year=now.year, hour=now.hour,
                minute=now.minute, second=now.second,
                microsecond=now.microsecond)


def unmarshall_time(tyme):
    """Unmarshall a datetime dict."""
    return datetime.datetime(day=tyme['day'],
                             month=tyme['month'],
                             year=tyme['year'],
                             hour=tyme['hour'],
                             minute=tyme['minute'],
                             second=tyme['second'],
                             microsecond=tyme['microsecond'])


def delta_seconds(before, after):
    """Return the difference between two timing objects.

    Compute the difference in seconds between two date, time, or
    datetime objects (as a float, to microsecond resolution).
    """
    delta = after - before
    try:
        return delta.total_seconds()
    except AttributeError:
        return ((delta.days * 24 * 3600) + delta.seconds +
                float(delta.microseconds) / (10 ** 6))


def is_soon(dt, window):
    """Determines if time is going to happen in the next window seconds.

    :params dt: the time
    :params window: minimum seconds to remain to consider the time not soon

    :return: True if expiration is within the given duration
    """
    soon = (utcnow() + datetime.timedelta(seconds=window))
    return normalize_time(dt) <= soon

def datetime_now():
    return time.strftime('%Y-%m-%d %H:%M:%S')
