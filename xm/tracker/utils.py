import math
from mx.DateTime import DateTimeDeltaFrom


def round_time_to_minutes(time):
    """Show the time, rounded up/down to minutes.

    The argument must be an mx.DateTimeDelta:

      >>> round_time_to_minutes('04:50')
      Traceback (most recent call last):
      ...
      Exception: time must be an mx.DateTimeDelta

    For testing we display the return value in a readable format,
    using hours, minutes and seconds:

      >>> fmt = '%H:%M:%S'
      >>> time = DateTimeDeltaFrom(hours=1, minutes=37, seconds=29)
      >>> round_time_to_minutes(time).strftime(fmt)
      '01:38:00'

    Even one second should be rounded up to one minute:

      >>> time = DateTimeDeltaFrom(hours=0, minutes=0, seconds=1)
      >>> round_time_to_minutes(time).strftime(fmt)
      '00:01:00'

    Zero seconds should stay at zero minutes though, otherwise the
    total time of a tracker task is already one minute when it has no
    entries.

      >>> time = DateTimeDeltaFrom(hours=0, minutes=0, seconds=0)
      >>> round_time_to_minutes(time).strftime(fmt)
      '00:00:00'

    """
    if not hasattr(time, 'absvalues'):
        raise Exception('time must be an mx.DateTimeDelta')
    minutes = math.ceil(time.minutes)
    return DateTimeDeltaFrom(minutes=minutes)


def round_time_to_quarter_hours(time):
    """Show the time, rounded up/down to quarter hours.

    The argument must be an mx.DateTimeDelta:

      >>> round_time_to_quarter_hours('04:50')
      Traceback (most recent call last):
      ...
      Exception: time must be an mx.DateTimeDelta

    For testing we display the return value in a readable format,
    using hours, minutes and seconds:

      >>> fmt = '%H:%M:%S'
      >>> time = DateTimeDeltaFrom(hours=1, minutes=30, seconds=00)
      >>> round_time_to_quarter_hours(time).strftime(fmt)
      '01:30:00'
      >>> time = DateTimeDeltaFrom(hours=1, minutes=30, seconds=01)
      >>> round_time_to_quarter_hours(time).strftime(fmt)
      '01:45:00'
      >>> time = DateTimeDeltaFrom(hours=1, minutes=52, seconds=30)
      >>> round_time_to_quarter_hours(time).strftime(fmt)
      '02:00:00'

    """
    if not hasattr(time, 'absvalues'):
        raise Exception('time must be an mx.DateTimeDelta')

    minutes = int(math.ceil(time.minutes / 15.0) * 15)
    return DateTimeDeltaFrom(minutes=minutes)
