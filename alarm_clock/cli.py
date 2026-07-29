import argparse
import sys

from alarm_clock.models import Alarm
from alarm_clock.utils import validate_time_format, is_time_in_future
from alarm_clock.storage import add_alarm, get_alarm_by_id, load_alarms, delete_alarm as storage_delete_alarm, snooze_alarm
from alarm_clock.core import start_monitoring

def set_alarm(args: argparse.Namespace) -> None:
    """Handle the 'set' subcommand."""
    if not validate_time_format(args.time):
        print(f"Error: Invalid time format '{args.time}'. Must be YYYY-MM-DD HH:MM (24-hour).")
        sys.exit(1)
        
    if not is_time_in_future(args.time):
        print(f"Error: The alarm time '{args.time}' has already passed. Please set a future time.")
        sys.exit(1)
        
    alarm = Alarm(time=args.time, label=args.label)
    add_alarm(alarm)
    print(f"Alarm set successfully!")
    print(f"ID: {alarm.id}")
    print(f"Time: {alarm.time}")
    print(f"Label: {alarm.label}")

def list_alarms(args: argparse.Namespace) -> None:
    """Handle the 'list' subcommand."""
    alarms = load_alarms()
    if not alarms:
        print("No pending alarms.")
        return
        
    print(f"{'ID':<10} | {'Time':<16} | {'Status':<8} | {'Label'}")
    print("-" * 60)
    for alarm in alarms:
        status = "Active" if alarm.is_active else "Inactive"
        print(f"{alarm.id:<10} | {alarm.time:<16} | {status:<8} | {alarm.label}")

def delete_alarm_cli(args: argparse.Namespace) -> None:
    """Handle the 'delete' subcommand."""
    alarm = get_alarm_by_id(args.id)
    if not alarm:
        print(f"Error: Alarm with ID '{args.id}' not found.")
        sys.exit(1)
        
    if storage_delete_alarm(args.id):
        print(f"Alarm {args.id} deleted successfully.")
    else:
        print(f"Error: Failed to delete alarm {args.id}.")
        sys.exit(1)

def snooze_alarm_cli(args: argparse.Namespace) -> None:
    """Handle the 'snooze' subcommand."""
    alarm = snooze_alarm(args.id, args.minutes)
    if not alarm:
        print(f"Error: Alarm with ID '{args.id}' not found.")
        sys.exit(1)
        
    print(f"Alarm {alarm.id} snoozed for {args.minutes} minutes.")
    print(f"New time: {alarm.time}")

def run_alarms(args: argparse.Namespace) -> None:
    """Handle the 'run' subcommand."""
    start_monitoring()

def setup_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Alarm Clock CLI Application"
    )
    
    subparsers = parser.add_subparsers(title="commands", dest="command")
    subparsers.required = True

    # 'set' command
    parser_set = subparsers.add_parser("set", help="Set a new alarm")
    parser_set.add_argument("time", help="Time in YYYY-MM-DD HH:MM format (24-hour)")
    parser_set.add_argument("label", nargs="?", default="Alarm", help="Optional label for the alarm")
    parser_set.set_defaults(func=set_alarm)

    # 'list' command
    parser_list = subparsers.add_parser("list", help="List all pending alarms")
    parser_list.set_defaults(func=list_alarms)

    # 'delete' command
    parser_delete = subparsers.add_parser("delete", help="Delete an alarm by ID")
    parser_delete.add_argument("id", help="The ID (or prefix) of the alarm to delete")
    parser_delete.set_defaults(func=delete_alarm_cli)

    # 'snooze' command
    parser_snooze = subparsers.add_parser("snooze", help="Snooze an alarm by adding minutes to its time")
    parser_snooze.add_argument("id", help="The ID (or prefix) of the alarm to snooze")
    parser_snooze.add_argument("minutes", type=int, nargs="?", default=5, help="Minutes to snooze (default: 5)")
    parser_snooze.set_defaults(func=snooze_alarm_cli)

    # 'run' command
    parser_run = subparsers.add_parser("run", help="Start the background monitoring process to trigger alarms")
    parser_run.set_defaults(func=run_alarms)

    return parser

def main() -> None:
    """Main entry point for the CLI."""
    parser = setup_parser()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    # Call the default function set for the parsed subcommand
    args.func(args)
