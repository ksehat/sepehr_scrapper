from datetime import datetime
from persiantools.jdatetime import JalaliDateTime


def persian_to_datetime(persian_date_str):
    if ' ' in persian_date_str:
        year, month, day = map(int, persian_date_str.split(' ')[0].split("/"))
    else:
        year, month, day = map(int, persian_date_str.split("/"))

    persian_date = JalaliDateTime(year, month, day)
    christian_date = persian_date.to_gregorian()

    return christian_date.date()


def persian_time_to_datetime(persian_time_str):
    if ' ' in persian_time_str:
        year, month, day = map(int, persian_time_str.split(' ')[1].split(":"))
    else:
        hour, minute = map(int, persian_time_str.split(":"))

    today = datetime.now().date()

    return datetime(today.year, today.month, today.day, hour, minute).time()
