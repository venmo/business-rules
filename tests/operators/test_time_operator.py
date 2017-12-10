from datetime import time, datetime, timedelta

from business_rules.operators import TimeType
from .. import TestCase


class TimeOperatorTests(TestCase):
    def setUp(self):
        super(TimeOperatorTests, self).setUp()
        self.TEST_HOUR = 13
        self.TEST_MINUTE = 55
        self.TEST_SECOND = 25
        self.TEST_TIME = '{hour}:{minute}:{second}'.format(
            hour=self.TEST_HOUR, minute=self.TEST_MINUTE, second=self.TEST_SECOND
        )
        self.TEST_TIME_OBJ = time(self.TEST_HOUR, self.TEST_MINUTE, self.TEST_SECOND)
        self.TEST_DATETIME_OBJ = datetime(2017, 1, 1, hour=self.TEST_HOUR, minute=self.TEST_MINUTE,
                                          second=self.TEST_SECOND)

    def test_instantiate(self):
        err_string = "foo is not a valid time type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            TimeType("foo")

    def test_time_type_validates_and_cast_time(self):
        result = TimeType(self.TEST_TIME)
        self.assertTrue(isinstance(result.value, time))

        result = TimeType(self.TEST_DATETIME_OBJ)
        self.assertTrue(isinstance(result.value, time))

    def test_time_equal_to(self):
        self.assertTrue(TimeType(self.TEST_TIME).equal_to(self.TEST_TIME))
        self.assertTrue(TimeType(self.TEST_TIME).equal_to(self.TEST_TIME_OBJ))
        self.assertTrue(TimeType(self.TEST_TIME_OBJ).equal_to(self.TEST_TIME_OBJ))
        self.assertTrue(TimeType(self.TEST_TIME_OBJ).equal_to(self.TEST_TIME))

    def test_other_value_not_time(self):
        error_string = "2016-10 is not a valid time type"
        with self.assertRaisesRegexp(AssertionError, error_string):
            TimeType(self.TEST_TIME).equal_to("2016-10")

    def test_time_after_than(self):
        self.assertTrue(TimeType(self.TEST_TIME).after_than(self._relative_time(self.TEST_TIME_OBJ, 0, 0, -1)))
        self.assertFalse(TimeType(self.TEST_TIME).after_than(self.TEST_TIME))
        self.assertFalse(TimeType(self.TEST_TIME).after_than(self._relative_time(self.TEST_TIME_OBJ, 0, 0, 1)))

    def test_time_after_than_or_equal_to(self):
        self.assertTrue(TimeType(self.TEST_TIME).after_than_or_equal_to(self.TEST_TIME))
        self.assertTrue(
            TimeType(self.TEST_TIME).after_than_or_equal_to(self._relative_time(self.TEST_TIME_OBJ, 0, 0, -1))
        )
        self.assertFalse(
            TimeType(self.TEST_TIME).after_than_or_equal_to(self._relative_time(self.TEST_TIME_OBJ, 0, 0, 1))
        )

    def test_time_before_than(self):
        self.assertFalse(TimeType(self.TEST_TIME).before_than(self._relative_time(self.TEST_TIME_OBJ, 0, 0, -1)))
        self.assertFalse(TimeType(self.TEST_TIME).before_than(self.TEST_TIME))
        self.assertTrue(TimeType(self.TEST_TIME).before_than(self._relative_time(self.TEST_TIME_OBJ, 0, 0, 1)))

    def test_time_before_than_or_equal_to(self):
        self.assertTrue(TimeType(self.TEST_TIME).before_than_or_equal_to(self.TEST_TIME))
        self.assertFalse(
            TimeType(self.TEST_TIME_OBJ).before_than_or_equal_to(self._relative_time(self.TEST_TIME_OBJ, 0, 0, -1))
        )
        self.assertTrue(
            TimeType(self.TEST_TIME).before_than_or_equal_to(self._relative_time(self.TEST_TIME_OBJ, 0, 0, 1)))

    @staticmethod
    def _relative_time(base_time, hours, minutes, seconds):
        return time(base_time.hour+hours, base_time.minute+minutes, base_time.second+seconds)
