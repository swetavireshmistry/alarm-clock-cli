import datetime

def validate_time_format(time_str: str) -> bool:
    """Validate if the string is in YYYY-MM-DD HH:MM format."""
    try:
        datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def is_time_in_future(time_str: str) -> bool:
    """Check if the given YYYY-MM-DD HH:MM time is in the future."""
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    return dt > datetime.datetime.now()

def get_next_alarm_datetime(time_str: str) -> datetime.datetime:
    """
    Get the datetime object for the given YYYY-MM-DD HH:MM time.
    """
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")

def add_minutes_to_time(time_str: str, minutes: int) -> str:
    """Add a given number of minutes to a YYYY-MM-DD HH:MM time string and return the new string."""
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    dt += datetime.timedelta(minutes=minutes)
    return dt.strftime("%Y-%m-%d %H:%M")
