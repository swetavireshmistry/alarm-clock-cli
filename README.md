# Alarm Clock CLI

A lightweight, robust, and clean Alarm Clock command-line application built in Python. Focusing on code quality, clean architecture, and maintainability.

## Features
- **Set Alarms**: Add new alarms with custom labels using 24-hour time format.
- **List Alarms**: View all pending alarms in a clear tabular format.
- **Snooze Alarms**: Snooze an alarm by ID to push it forward by a specified number of minutes.
- **Delete Alarms**: Remove alarms by their unique ID.
- **Run Monitor**: A background process that polls for triggered alarms and alerts the user with a terminal bell.
- **Persistent Storage**: Alarms are saved to a JSON file (`alarm_clock/alarms.json`) so they survive application restarts.

## Assumptions
- Alarms are one-off and do not recur.
- Time is entered and evaluated in the local system timezone.
- A 24-hour time format (HH:MM) is used.
- If an alarm is set for a time that has already passed today, it is automatically scheduled for tomorrow.
- The monitoring loop (`run` command) runs in the foreground of a terminal session.

## Architecture & Design Decisions
The application strictly uses the Python Standard Library (3.11+) and avoids unnecessary complexity.

- **Folder Structure**: Separated into `cli.py` (interface), `core.py` (business logic), `storage.py` (data access), and `models.py` (data structures). This adheres to the Single Responsibility Principle.
- **`argparse`**: Used for robust CLI argument parsing and automatic help generation.
- **Data Storage**: A simple JSON file is used. It's lightweight, human-readable, and perfect for simple structured data. A full database like SQLite would be over-engineering for this scope.
- **Polling Strategy**: The `run` command uses a simple blocking `time.sleep` loop. Since it's a CLI app without a GUI, multithreading or asyncio is not required and would introduce unnecessary complexity and race conditions.
- **Data Classes**: The `Alarm` class uses `dataclasses` for clean, typed representations of alarm data.

## Excluded Features (Intentional)
- **GUI/React/Web Frameworks**: Excluded per constraints to focus on core Python engineering.
- **Database (SQLite/Postgres)**: Overkill for simple alarm persistence.
- **Multithreading**: Not needed for a foreground blocking loop.
- **Recurring Alarms**: Excluded to keep the solution simple and completable within the ~30-minute time constraint.

## Installation
Ensure you have Python 3.11+ installed.

```bash
# Clone or download the repository
cd alarm-clock

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows

# Install requirements
pip install -r requirements.txt
```

## Usage

### 1. Set an Alarm
```bash
python3 main.py set 07:30 "Wake up"
python3 main.py set 14:00 "Meeting"
```

### 2. List Alarms
```bash
python3 main.py list
```

### 3. Delete an Alarm
You can use the full ID or just a prefix of the ID.
```bash
python3 main.py delete 5a3f
```

### 4. Snooze an Alarm
You can snooze an alarm by ID (default is 5 minutes).
```bash
# Snooze for 5 minutes
python3 main.py snooze 5a3f

# Snooze for 10 minutes
python3 main.py snooze 5a3f 10
```

### 5. Run the Alarm Monitor
This command will block the terminal and wait for alarms to trigger.
```bash
python3 main.py run
```
*Note: Press `Ctrl+C` to stop monitoring.*

## Running Tests
Unit tests are implemented using the standard `unittest` framework. To run the tests:

```bash
python3 -m unittest discover tests
```

