import json
from pathlib import Path
from typing import List, Optional
from alarm_clock.models import Alarm

DEFAULT_STORAGE_FILE = Path(__file__).parent / "alarms.json"

def get_storage_file() -> Path:
    """Get the storage file path."""
    return DEFAULT_STORAGE_FILE

def load_alarms(storage_file: Path = None) -> List[Alarm]:
    """Load all alarms from the storage file."""
    if storage_file is None:
        storage_file = get_storage_file()
        
    if not storage_file.exists():
        return []
        
    try:
        with open(storage_file, "r") as f:
            data = json.load(f)
            return [Alarm.from_dict(item) for item in data]
    except json.JSONDecodeError:
        # If file is corrupted, return empty list
        return []
    except IOError:
        return []

def save_alarms(alarms: List[Alarm], storage_file: Path = None) -> None:
    """Save alarms to the storage file."""
    if storage_file is None:
        storage_file = get_storage_file()
        
    data = [alarm.to_dict() for alarm in alarms]
    try:
        with open(storage_file, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving alarms: {e}")

def add_alarm(alarm: Alarm, storage_file: Path = None) -> None:
    """Add a new alarm to storage."""
    alarms = load_alarms(storage_file)
    alarms.append(alarm)
    save_alarms(alarms, storage_file)

def delete_alarm(alarm_id: str, storage_file: Path = None) -> bool:
    """
    Delete an alarm by ID. 
    Returns True if deleted, False if not found.
    """
    alarms = load_alarms(storage_file)
    initial_length = len(alarms)
    
    # Filter out the alarm to delete
    alarms = [a for a in alarms if a.id != alarm_id and not a.id.startswith(alarm_id)]
    
    if len(alarms) < initial_length:
        save_alarms(alarms, storage_file)
        return True
    return False

def deactivate_alarm(alarm_id: str, storage_file: Path = None) -> bool:
    """Soft delete an alarm by setting it to inactive."""
    alarms = load_alarms(storage_file)
    for alarm in alarms:
        if alarm.id == alarm_id or alarm.id.startswith(alarm_id):
            alarm.is_active = False
            save_alarms(alarms, storage_file)
            return True
    return False

def get_alarm_by_id(alarm_id: str, storage_file: Path = None) -> Optional[Alarm]:
    """Get an alarm by its ID prefix."""
    alarms = load_alarms(storage_file)
    for alarm in alarms:
        if alarm.id == alarm_id or alarm.id.startswith(alarm_id):
            return alarm
    return None

def snooze_alarm(alarm_id: str, minutes: int, storage_file: Path = None) -> Optional[Alarm]:
    """Snooze an alarm by adding minutes to its time and reactivating it."""
    from alarm_clock.utils import add_minutes_to_time
    alarms = load_alarms(storage_file)
    for alarm in alarms:
        if alarm.id == alarm_id or alarm.id.startswith(alarm_id):
            alarm.time = add_minutes_to_time(alarm.time, minutes)
            alarm.is_active = True
            save_alarms(alarms, storage_file)
            return alarm
    return None
