import unittest
import datetime
from unittest.mock import patch
from alarm_clock.utils import validate_time_format, get_next_alarm_datetime

class TestUtils(unittest.TestCase):
    
    def test_validate_time_format_valid(self):
        self.assertTrue(validate_time_format("12:30"))
        self.assertTrue(validate_time_format("00:00"))
        self.assertTrue(validate_time_format("23:59"))
        
    def test_validate_time_format_invalid(self):
        self.assertFalse(validate_time_format("24:00"))
        self.assertFalse(validate_time_format("12:60"))
        self.assertFalse(validate_time_format("abc"))
        
    @patch('alarm_clock.utils.datetime')
    def test_get_next_alarm_datetime_today(self, mock_datetime):
        mock_now = datetime.datetime(2023, 10, 27, 10, 0)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.strptime = datetime.datetime.strptime
        mock_datetime.datetime.combine = datetime.datetime.combine
        mock_datetime.timedelta = datetime.timedelta
        
        # Alarm at 12:00 should be today
        result = get_next_alarm_datetime("12:00")
        expected = datetime.datetime(2023, 10, 27, 12, 0)
        self.assertEqual(result, expected)
        
    @patch('alarm_clock.utils.datetime')
    def test_get_next_alarm_datetime_tomorrow(self, mock_datetime):
        # Mock current time to be 14:00
        mock_now = datetime.datetime(2023, 10, 27, 14, 0)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.datetime.strptime = datetime.datetime.strptime
        mock_datetime.datetime.combine = datetime.datetime.combine
        mock_datetime.timedelta = datetime.timedelta
        
        # Alarm at 12:00 should be tomorrow
        result = get_next_alarm_datetime("12:00")
        expected = datetime.datetime(2023, 10, 28, 12, 0)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
