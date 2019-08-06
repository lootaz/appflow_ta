import datetime


def convert_age_to_timedelta(age: str) -> datetime.timedelta:
    delta = datetime.timedelta()

    try:
        value = int(age.split()[0])
    except ValueError:
        return delta

    if 'second' in age:
        delta = datetime.timedelta(seconds=value)
    elif 'minute' in age:
        delta = datetime.timedelta(minutes=value)
    elif 'hour' in age:
        delta = datetime.timedelta(hours=value)
    elif 'day' in age:
        delta = datetime.timedelta(days=value)
    elif 'week' in age:
        delta = datetime.timedelta(weeks=value)

    return delta
