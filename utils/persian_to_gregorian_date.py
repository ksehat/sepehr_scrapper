from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
import persiantools

import pyarabic

def normalize_persian_text(text):
  normalized_text = text.replace('ي', 'ی')
  return normalized_text


def persian_to_datetime(persian_date_str):
    if ':' in persian_date_str:
        persian_date_str = persian_date_str.split(' ')[0]
    try:
        parts = persian_date_str.split('/')

        if len(parts) == 3:
            # Check if it's in the format 'DD/MM/YYYY'
            if parts[1].isdigit():
                year, month, day = map(int, parts)
            else:
                # Handle format 'DD/month_name/YYYY' (using persiantools)
                year = int(parts[2])
                month = int(persiantools.jdatetime.MONTH_NAMES_FA.index(normalize_persian_text(parts[1])))
                day = int(parts[0])
        else:
            return persian_date_str

        persian_date = JalaliDateTime(year, month, day)
        christian_date = persian_date.to_gregorian()

        return christian_date.date()
    except:
        return persian_date_str


def persian_time_to_datetime(persian_time_str):
    if ':' in persian_time_str:
        try:
            hour, minute = map(int, persian_time_str.split(' ')[1].split(":"))
        except:
            hour, minute = map(int, persian_time_str.split(":"))

    today = datetime.now().date()

    return datetime(today.year, today.month, today.day, hour, minute).time()
