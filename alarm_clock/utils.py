import datetime

def validate_time_format(time_str: str) -> bool:
    """Validate if the string is in HH:MM format."""
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def get_next_alarm_datetime(time_str: str) -> datetime.datetime:
    """
    Get the next datetime object for the given HH:MM time.
    If the time has passed today, it schedules for tomorrow.
    """
    now = datetime.datetime.now()
    alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
    
    alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)
    
    # If the time has already passed today, set it for tomorrow
    if alarm_datetime <= now:
        alarm_datetime += datetime.timedelta(days=1)
        
    return alarm_datetime

def add_minutes_to_time(time_str: str, minutes: int) -> str:
    """Add a given number of minutes to an HH:MM time string and return the new HH:MM."""
    dt = datetime.datetime.strptime(time_str, "%H:%M")
    dt += datetime.timedelta(minutes=minutes)
    return dt.strftime("%H:%M")
