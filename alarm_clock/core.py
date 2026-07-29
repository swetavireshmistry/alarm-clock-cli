import time
import datetime
import sys
from typing import List, Tuple
from pathlib import Path

import subprocess
from alarm_clock.models import Alarm
from alarm_clock.storage import load_alarms, delete_alarm, deactivate_alarm
from alarm_clock.utils import get_next_alarm_datetime



def trigger_alarm(alarm: Alarm) -> None:
    """Trigger the alarm by printing a message and playing a sound/voice."""
    print(f"\n\a[ALARM TRIGGERED] {alarm.time} - {alarm.label}")

    try:
        subprocess.run(
            ["spd-say", f"Alarm! {alarm.label}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        # Fallback if spd-say is not installed
        pass

def start_monitoring(storage_file: Path = None, interval: int = 1) -> None:
    """
    Start the background monitoring process.
    Continuously polls for alarms and triggers them if the time has passed.
    """
    print("Monitoring alarms... (Press Ctrl+C to stop)")
    
    known_alarms = {}
    
    try:
        while True:
            now = datetime.datetime.now()
            alarms = load_alarms(storage_file)
            current_ids = {alarm.id for alarm in alarms}
            
            # Clean up deleted alarms
            known_alarms = {k: v for k, v in known_alarms.items() if k in current_ids}
            
            # Identify alarms that should trigger
            triggered = []
            for alarm in alarms:
                if not alarm.is_active:
                    continue
                if alarm.id not in known_alarms:
                    try:
                        known_alarms[alarm.id] = get_next_alarm_datetime(alarm.time)
                    except ValueError:
                        continue
                        
                alarm_dt = known_alarms[alarm.id]
                if now >= alarm_dt:
                    triggered.append(alarm)
                    
            # Process triggered alarms
            for alarm in triggered:
                trigger_alarm(alarm)
                # Soft delete from storage after triggering
                deactivate_alarm(alarm.id, storage_file)
                
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nStopping alarm monitor.")
        sys.exit(0)
