import unittest
import datetime
from alarm_clock.utils import validate_time_format, get_next_alarm_datetime, add_minutes_to_time

class TestUtils(unittest.TestCase):
    
    def test_validate_time_format_valid(self):
        self.assertTrue(validate_time_format("2023-10-27 12:30"))
        self.assertTrue(validate_time_format("2023-01-01 00:00"))
        
    def test_validate_time_format_invalid(self):
        self.assertFalse(validate_time_format("12:30"))
        self.assertFalse(validate_time_format("2023-10-27 24:00"))
        self.assertFalse(validate_time_format("2023-13-01 12:00"))
        self.assertFalse(validate_time_format("abc"))
        
    def test_get_next_alarm_datetime(self):
        result = get_next_alarm_datetime("2023-10-27 12:00")
        expected = datetime.datetime(2023, 10, 27, 12, 0)
        self.assertEqual(result, expected)

    def test_add_minutes_to_time(self):
        result = add_minutes_to_time("2023-10-27 12:00", 5)
        self.assertEqual(result, "2023-10-27 12:05")
        
        result_rollover = add_minutes_to_time("2023-10-27 23:58", 5)
        self.assertEqual(result_rollover, "2023-10-28 00:03")

if __name__ == "__main__":
    unittest.main()
