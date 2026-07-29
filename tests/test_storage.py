import unittest
import os
import json
from pathlib import Path
from alarm_clock.models import Alarm
from alarm_clock.storage import load_alarms, save_alarms, add_alarm, delete_alarm, get_alarm_by_id

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        self.test_file = Path("test_alarms.json")
        if self.test_file.exists():
            os.remove(self.test_file)
            
    def tearDown(self):
        if self.test_file.exists():
            os.remove(self.test_file)
            
    def test_save_and_load_alarms(self):
        alarm1 = Alarm(time="08:00", label="Morning")
        alarm2 = Alarm(time="12:00", label="Lunch")
        
        save_alarms([alarm1, alarm2], storage_file=self.test_file)
        
        self.assertTrue(self.test_file.exists())
        
        loaded = load_alarms(storage_file=self.test_file)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].id, alarm1.id)
        self.assertEqual(loaded[1].time, "12:00")
        
    def test_load_empty_or_missing(self):
        loaded = load_alarms(storage_file=self.test_file)
        self.assertEqual(loaded, [])
        
    def test_add_alarm(self):
        alarm = Alarm(time="15:00", label="Tea")
        add_alarm(alarm, storage_file=self.test_file)
        
        loaded = load_alarms(storage_file=self.test_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].time, "15:00")
        
    def test_delete_alarm(self):
        alarm = Alarm(time="15:00", label="Tea")
        add_alarm(alarm, storage_file=self.test_file)
        
        result = delete_alarm(alarm.id, storage_file=self.test_file)
        self.assertTrue(result)
        
        loaded = load_alarms(storage_file=self.test_file)
        self.assertEqual(len(loaded), 0)
        
        result2 = delete_alarm("invalid_id", storage_file=self.test_file)
        self.assertFalse(result2)

if __name__ == "__main__":
    unittest.main()
