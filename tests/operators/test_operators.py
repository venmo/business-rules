from __future__ import absolute_import
import sys
from datetime import datetime, timedelta, date, time
from decimal import Decimal

import pytz

from business_rules.operators import (
    StringType,
    NumericType,
    BooleanType,
    SelectType,
    SelectMultipleType,
    BaseType,
    DateTimeType,
    TimeType,
)
from tests import TestCase


class BaseTypeOperatorTests(TestCase):
    def test_base_type_cannot_be_created(self):
        with self.assertRaises(NotImplementedError):
            BaseType('test')


class StringOperatorTests(TestCase):
    def test_invalid_value(self):
        with self.assertRaises(AssertionError):
            StringType(123)

    def test_operator_decorator(self):
        self.assertTrue(StringType("foo").equal_to.is_operator)

    def test_string_equal_to(self):
        self.assertTrue(StringType("foo").equal_to("foo"))
        self.assertFalse(StringType("foo").equal_to("Foo"))

    def test_string_equal_to_case_insensitive(self):
        self.assertTrue(StringType("foo").equal_to_case_insensitive("FOo"))
        self.assertTrue(StringType("foo").equal_to_case_insensitive("foo"))
        self.assertFalse(StringType("foo").equal_to_case_insensitive("blah"))

    def test_string_starts_with(self):
        self.assertTrue(StringType("hello").starts_with("he"))
        self.assertFalse(StringType("hello").starts_with("hey"))
        self.assertFalse(StringType("hello").starts_with("He"))

    def test_string_ends_with(self):
        self.assertTrue(StringType("hello").ends_with("lo"))
        self.assertFalse(StringType("hello").ends_with("boom"))
        self.assertFalse(StringType("hello").ends_with("Lo"))

    def test_string_contains(self):
        self.assertTrue(StringType("hello").contains("ell"))
        self.assertTrue(StringType("hello").contains("he"))
        self.assertTrue(StringType("hello").contains("lo"))
        self.assertFalse(StringType("hello").contains("asdf"))
        self.assertFalse(StringType("hello").contains("ElL"))

    def test_string_matches_regex(self):
        self.assertTrue(StringType("hello").matches_regex(r"^h"))
        self.assertFalse(StringType("hello").matches_regex(r"^sh"))

    def test_non_empty(self):
        self.assertTrue(StringType("hello").non_empty())
        self.assertFalse(StringType("").non_empty())
        self.assertFalse(StringType(None).non_empty())


class NumericOperatorTests(TestCase):
    def test_instantiate(self):
        err_string = "foo is not a valid numeric type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            NumericType("foo")

    def test_numeric_type_validates_and_casts_decimal(self):
        ten_dec = Decimal(10)
        ten_int = 10
        ten_float = 10.0
        if sys.version_info[0] == 2:
            ten_long = int(10)
        else:
            ten_long = int(10)  # long and int are same in python3
        ten_var_dec = NumericType(ten_dec)  # this should not throw an exception
        ten_var_int = NumericType(ten_int)
        ten_var_float = NumericType(ten_float)
        ten_var_long = NumericType(ten_long)
        self.assertTrue(isinstance(ten_var_dec.value, Decimal))
        self.assertTrue(isinstance(ten_var_int.value, Decimal))
        self.assertTrue(isinstance(ten_var_float.value, Decimal))
        self.assertTrue(isinstance(ten_var_long.value, Decimal))

    def test_numeric_equal_to(self):
        self.assertTrue(NumericType(10).equal_to(10))
        self.assertTrue(NumericType(10).equal_to(10.0))
        self.assertTrue(NumericType(10).equal_to(10.000001))
        self.assertTrue(NumericType(10.000001).equal_to(10))
        self.assertTrue(NumericType(Decimal('10.0')).equal_to(10))
        self.assertTrue(NumericType(10).equal_to(Decimal('10.0')))
        self.assertFalse(NumericType(10).equal_to(10.00001))
        self.assertFalse(NumericType(10).equal_to(11))

    def test_other_value_not_numeric(self):
        error_string = "10 is not a valid numeric type"
        with self.assertRaisesRegexp(AssertionError, error_string):
            NumericType(10).equal_to("10")

    def test_numeric_greater_than(self):
        self.assertTrue(NumericType(10).greater_than(1))
        self.assertFalse(NumericType(10).greater_than(11))
        self.assertTrue(NumericType(10.1).greater_than(10))
        self.assertFalse(NumericType(10.000001).greater_than(10))
        self.assertTrue(NumericType(10.000002).greater_than(10))

    def test_numeric_greater_than_or_equal_to(self):
        self.assertTrue(NumericType(10).greater_than_or_equal_to(1))
        self.assertFalse(NumericType(10).greater_than_or_equal_to(11))
        self.assertTrue(NumericType(10.1).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10.000001).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10.000002).greater_than_or_equal_to(10))
        self.assertTrue(NumericType(10).greater_than_or_equal_to(10))

    def test_numeric_less_than(self):
        self.assertTrue(NumericType(1).less_than(10))
        self.assertFalse(NumericType(11).less_than(10))
        self.assertTrue(NumericType(10).less_than(10.1))
        self.assertFalse(NumericType(10).less_than(10.000001))
        self.assertTrue(NumericType(10).less_than(10.000002))

    def test_numeric_less_than_or_equal_to(self):
        self.assertTrue(NumericType(1).less_than_or_equal_to(10))
        self.assertFalse(NumericType(11).less_than_or_equal_to(10))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.1))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.000001))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10.000002))
        self.assertTrue(NumericType(10).less_than_or_equal_to(10))


class BooleanOperatorTests(TestCase):
    def test_instantiate(self):
        err_string = "foo is not a valid boolean type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            BooleanType("foo")
        err_string = "None is not a valid boolean type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            BooleanType(None)

    def test_boolean_is_true_and_is_false(self):
        self.assertTrue(BooleanType(True).is_true())
        self.assertFalse(BooleanType(True).is_false())
        self.assertFalse(BooleanType(False).is_true())
        self.assertTrue(BooleanType(False).is_false())


class SelectOperatorTests(TestCase):
    def test_invalid_value(self):
        with self.assertRaises(AssertionError):
            SelectType(123)

    def test_contains(self):
        self.assertTrue(SelectType([1, 2]).contains(2))
        self.assertFalse(SelectType([1, 2]).contains(3))
        self.assertTrue(SelectType([1, 2, "a"]).contains("A"))

    def test_does_not_contain(self):
        self.assertTrue(SelectType([1, 2]).does_not_contain(3))
        self.assertFalse(SelectType([1, 2]).does_not_contain(2))
        self.assertFalse(SelectType([1, 2, "a"]).does_not_contain("A"))


class SelectMultipleOperatorTests(TestCase):
    def test_invalid_value(self):
        with self.assertRaises(AssertionError):
            SelectMultipleType(123)

    def test_contains_all(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        contains_all([2, 1]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         contains_all([2, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        contains_all([2, 1, "A"]))

    def test_is_contained_by(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        is_contained_by([2, 1, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         is_contained_by([2, 3, 4]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        is_contained_by([2, 1, "A"]))

    def test_shares_at_least_one_element_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_at_least_one_element_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_at_least_one_element_with([4, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        shares_at_least_one_element_with([4, "A"]))

    def test_shares_exactly_one_element_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_exactly_one_element_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_exactly_one_element_with([4, 3]))
        self.assertTrue(SelectMultipleType([1, 2, "a"]).
                        shares_exactly_one_element_with([4, "A"]))
        self.assertFalse(SelectMultipleType([1, 2, 3]).
                         shares_exactly_one_element_with([2, 3, "a"]))

    def test_shares_no_elements_with(self):
        self.assertTrue(SelectMultipleType([1, 2]).
                        shares_no_elements_with([4, 3]))
        self.assertFalse(SelectMultipleType([1, 2]).
                         shares_no_elements_with([2, 3]))
        self.assertFalse(SelectMultipleType([1, 2, "a"]).
                         shares_no_elements_with([4, "A"]))


class DateTimeOperatorTests(TestCase):
    def setUp(self):
        super(DateTimeOperatorTests, self).setUp()
        self.TEST_YEAR = 2017
        self.TEST_MONTH = 1
        self.TEST_DAY = 16
        self.TEST_HOUR = 13
        self.TEST_MINUTE = 55
        self.TEST_SECOND = 25
        self.TEST_DATETIME = '{year}-0{month}-{day}T{hour}:{minute}:{second}'.format(
            year=self.TEST_YEAR, month=self.TEST_MONTH, day=self.TEST_DAY, hour=self.TEST_HOUR, minute=self.TEST_MINUTE,
            second=self.TEST_SECOND
        )
        self.TEST_DATE = '{year}-0{month}-{day}'.format(
            year=self.TEST_YEAR, month=self.TEST_MONTH, day=self.TEST_DAY
        )
        self.TEST_DATETIME_OBJ = datetime(self.TEST_YEAR, self.TEST_MONTH, self.TEST_DAY, self.TEST_HOUR,
                                          self.TEST_MINUTE, self.TEST_SECOND)
        self.TEST_DATE_OBJ = date(self.TEST_YEAR, self.TEST_MONTH, self.TEST_DAY)

        self.TEST_DATETIME_UTC_OBJ = datetime(self.TEST_YEAR, self.TEST_MONTH, self.TEST_DAY, self.TEST_HOUR,
                                              self.TEST_MINUTE, self.TEST_SECOND, tzinfo=pytz.UTC)

        self.datetime_type_date = DateTimeType(self.TEST_DATE)
        self.datetime_type_datetime = DateTimeType(self.TEST_DATETIME)
        self.datetime_type_datetime_obj = DateTimeType(self.TEST_DATETIME_OBJ)
        self.datetime_type_datetime_utc_obj = DateTimeType(self.TEST_DATETIME_UTC_OBJ)

    def test_instantiate(self):
        err_string = "foo is not a valid datetime type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            DateTimeType("foo")

    def test_datetime_type_validates_and_cast_datetime(self):
        result = DateTimeType(self.TEST_DATETIME)
        self.assertTrue(isinstance(result.value, datetime))

        result = DateTimeType(self.TEST_DATE)
        self.assertTrue(isinstance(result.value, datetime))

        result = DateTimeType(self.TEST_DATETIME_OBJ)
        self.assertTrue(isinstance(result.value, datetime))

        result = DateTimeType(self.TEST_DATE_OBJ)
        self.assertTrue(isinstance(result.value, datetime))

    def test_datetime_equal_to(self):
        self.assertTrue(self.datetime_type_datetime.equal_to(self.TEST_DATETIME))
        self.assertTrue(self.datetime_type_datetime.equal_to(self.TEST_DATETIME_OBJ))
        self.assertTrue(self.datetime_type_datetime.equal_to(self.TEST_DATETIME_UTC_OBJ))

        self.assertTrue(self.datetime_type_datetime_obj.equal_to(self.TEST_DATETIME))
        self.assertTrue(self.datetime_type_datetime_obj.equal_to(self.TEST_DATETIME_OBJ))
        self.assertTrue(self.datetime_type_datetime_obj.equal_to(self.TEST_DATETIME_UTC_OBJ))

        self.assertTrue(self.datetime_type_datetime_utc_obj.equal_to(self.TEST_DATETIME))
        self.assertTrue(self.datetime_type_datetime_utc_obj.equal_to(self.TEST_DATETIME_OBJ))
        self.assertTrue(self.datetime_type_datetime_utc_obj.equal_to(self.TEST_DATETIME_UTC_OBJ))

        self.assertTrue(self.datetime_type_date.equal_to(self.TEST_DATE))
        self.assertTrue(self.datetime_type_date.equal_to(self.TEST_DATE_OBJ))

    def test_other_value_not_datetime(self):
        error_string = "2016-10 is not a valid datetime type"
        with self.assertRaisesRegexp(AssertionError, error_string):
            DateTimeType(self.TEST_DATE).equal_to("2016-10")

    def datetime_after_than_asserts(self, datetime_type):
        # type: (DateTimeType) -> None
        self.assertFalse(datetime_type.after_than(self.TEST_DATETIME))
        self.assertFalse(datetime_type.after_than(self.TEST_DATETIME_OBJ))
        self.assertFalse(datetime_type.after_than(self.TEST_DATETIME_UTC_OBJ))
        self.assertTrue(datetime_type.after_than(self.TEST_DATETIME_OBJ - timedelta(seconds=1)))
        self.assertTrue(datetime_type.after_than(self.TEST_DATETIME_UTC_OBJ - timedelta(seconds=1)))
        self.assertFalse(datetime_type.after_than(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertFalse(datetime_type.after_than(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def test_datetime_after_than(self):
        self.datetime_after_than_asserts(self.datetime_type_datetime)
        self.datetime_after_than_asserts(self.datetime_type_datetime_obj)
        self.datetime_after_than_asserts(self.datetime_type_datetime_utc_obj)

        self.assertFalse(self.datetime_type_date.after_than(self.TEST_DATE))
        self.assertFalse(self.datetime_type_date.after_than(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertFalse(self.datetime_type_date.after_than(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def datetime_after_than_or_equal_to_asserts(self, datetime_type):
        # type: (DateTimeType) -> None
        self.assertTrue(datetime_type.after_than_or_equal_to(self.TEST_DATETIME))
        self.assertTrue(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_OBJ))
        self.assertTrue(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ))
        self.assertTrue(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_OBJ - timedelta(seconds=1)))
        self.assertFalse(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertTrue(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ - timedelta(seconds=1)))
        self.assertFalse(datetime_type.after_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def test_datetime_after_than_or_equal_to(self):
        self.assertTrue(self.datetime_type_date.after_than_or_equal_to(self.TEST_DATE))

        self.datetime_after_than_or_equal_to_asserts(self.datetime_type_datetime)
        self.datetime_after_than_or_equal_to_asserts(self.datetime_type_datetime_obj)
        self.datetime_after_than_or_equal_to_asserts(self.datetime_type_datetime_utc_obj)

    def datetime_before_than_asserts(self, datetime_type):
        # type: (DateTimeType) -> None
        self.assertFalse(datetime_type.before_than(self.TEST_DATETIME))
        self.assertFalse(datetime_type.before_than(self.TEST_DATETIME_OBJ))
        self.assertFalse(datetime_type.before_than(self.TEST_DATETIME_UTC_OBJ))
        self.assertFalse(datetime_type.before_than(self.TEST_DATETIME_OBJ - timedelta(seconds=1)))
        self.assertFalse(datetime_type.before_than(self.TEST_DATETIME_UTC_OBJ - timedelta(seconds=1)))
        self.assertTrue(datetime_type.before_than(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertTrue(datetime_type.before_than(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def test_datetime_before_than(self):
        self.datetime_before_than_asserts(self.datetime_type_datetime)
        self.datetime_before_than_asserts(self.datetime_type_datetime_obj)
        self.datetime_before_than_asserts(self.datetime_type_datetime_utc_obj)

        self.assertFalse(self.datetime_type_date.before_than(self.TEST_DATE))
        self.assertTrue(self.datetime_type_date.before_than(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertTrue(self.datetime_type_date.before_than(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def datetime_before_than_or_equal_to_asserts(self, datetime_type):
        # type: (DateTimeType) -> None
        self.assertTrue(datetime_type.before_than_or_equal_to(self.TEST_DATETIME))
        self.assertTrue(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_OBJ))
        self.assertTrue(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ))
        self.assertFalse(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_OBJ - timedelta(seconds=1)))
        self.assertFalse(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ - timedelta(seconds=1)))
        self.assertTrue(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertTrue(datetime_type.before_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1)))

    def test_datetime_before_than_or_equal_to(self):
        self.datetime_before_than_or_equal_to_asserts(self.datetime_type_datetime)
        self.datetime_before_than_or_equal_to_asserts(self.datetime_type_datetime_obj)
        self.datetime_before_than_or_equal_to_asserts(self.datetime_type_datetime_utc_obj)

        self.assertTrue(self.datetime_type_date.before_than_or_equal_to(self.TEST_DATE))
        self.assertTrue(self.datetime_type_date.before_than_or_equal_to(self.TEST_DATETIME_OBJ + timedelta(seconds=1)))
        self.assertTrue(
            self.datetime_type_date.before_than_or_equal_to(self.TEST_DATETIME_UTC_OBJ + timedelta(seconds=1))
        )


class TimeOperatorTests(TestCase):
    def setUp(self):
        super(TimeOperatorTests, self).setUp()
        self.TEST_HOUR = 13
        self.TEST_MINUTE = 55
        self.TEST_SECOND = 00
        self.TEST_TIME = '{hour}:{minute}:{second}'.format(
            hour=self.TEST_HOUR, minute=self.TEST_MINUTE, second=self.TEST_SECOND
        )
        self.TEST_TIME_NO_SECONDS = '{hour}:{minute}'.format(hour=self.TEST_HOUR, minute=self.TEST_MINUTE)
        self.TEST_TIME_OBJ = time(self.TEST_HOUR, self.TEST_MINUTE, self.TEST_SECOND)

        self.time_type_time = TimeType(self.TEST_TIME)
        self.time_type_time_no_seconds = TimeType(self.TEST_TIME_NO_SECONDS)
        self.time_type_time_obj = TimeType(self.TEST_TIME_OBJ)

    def test_instantiate(self):
        err_string = "foo is not a valid time type"
        with self.assertRaisesRegexp(AssertionError, err_string):
            TimeType("foo")

    def test_time_type_validates_and_cast_time(self):
        result = TimeType(self.TEST_TIME)
        self.assertTrue(isinstance(result.value, time))

        result = TimeType(self.TEST_TIME_NO_SECONDS)
        self.assertTrue(isinstance(result.value, time))

        result = TimeType(self.TEST_TIME_OBJ)
        self.assertTrue(isinstance(result.value, time))

    def test_time_equal_to(self):
        self.assertTrue(self.time_type_time_no_seconds.equal_to(self.TEST_TIME))
        self.assertTrue(self.time_type_time_no_seconds.equal_to(self.TEST_TIME_OBJ))

        self.assertTrue(self.time_type_time_obj.equal_to(self.TEST_TIME))
        self.assertTrue(self.time_type_time_obj.equal_to(self.TEST_TIME_OBJ))

        self.assertTrue(self.time_type_time.equal_to(self.TEST_TIME_NO_SECONDS))

    def test_other_value_not_time(self):
        error_string = "2016-10 is not a valid time type"
        with self.assertRaisesRegexp(AssertionError, error_string):
            TimeType(self.TEST_TIME_NO_SECONDS).equal_to("2016-10")

    def time_after_than_asserts(self, time_type):
        # type: (TimeType) -> None
        self.assertFalse(time_type.after_than(self.TEST_TIME))
        self.assertFalse(time_type.after_than(self.TEST_TIME_OBJ))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute - 1, 59)
        self.assertTrue(time_type.after_than(test_time))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertFalse(time_type.after_than(test_time))

    def test_time_after_than(self):
        self.time_after_than_asserts(self.time_type_time_no_seconds)
        self.time_after_than_asserts(self.time_type_time_obj)

        self.assertFalse(self.time_type_time.after_than(self.TEST_TIME_NO_SECONDS))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertFalse(self.time_type_time.after_than(test_time))

    def time_after_than_or_equal_to_asserts(self, time_type):
        # type: (TimeType) -> None
        self.assertTrue(time_type.after_than_or_equal_to(self.TEST_TIME))
        self.assertTrue(time_type.after_than_or_equal_to(self.TEST_TIME_OBJ))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute - 1, 59)
        self.assertTrue(time_type.after_than_or_equal_to(test_time))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertFalse(time_type.after_than_or_equal_to(test_time))

    def test_time_after_than_or_equal_to(self):
        self.assertTrue(self.time_type_time.after_than_or_equal_to(self.TEST_TIME_NO_SECONDS))

        self.time_after_than_or_equal_to_asserts(self.time_type_time_no_seconds)
        self.time_after_than_or_equal_to_asserts(self.time_type_time_obj)

    def time_before_than_asserts(self, time_type):
        # type: (TimeType) -> None
        self.assertFalse(time_type.before_than(self.TEST_TIME))
        self.assertFalse(time_type.before_than(self.TEST_TIME_OBJ))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute - 1, 59)
        self.assertFalse(time_type.before_than(test_time))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertTrue(time_type.before_than(test_time))

    def test_time_before_than(self):
        self.time_before_than_asserts(self.time_type_time_no_seconds)
        self.time_before_than_asserts(self.time_type_time_obj)

        self.assertFalse(self.time_type_time.before_than(self.TEST_TIME_NO_SECONDS))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertTrue(self.time_type_time.before_than(test_time))

    def time_before_than_or_equal_to_asserts(self, time_type):
        # type: (TimeType) -> None
        self.assertTrue(time_type.before_than_or_equal_to(self.TEST_TIME))
        self.assertTrue(time_type.before_than_or_equal_to(self.TEST_TIME_OBJ))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute - 1, 59)
        self.assertFalse(time_type.before_than_or_equal_to(test_time))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertTrue(time_type.before_than_or_equal_to(test_time))

    def test_time_before_than_or_equal_to(self):
        self.time_before_than_or_equal_to_asserts(self.time_type_time_no_seconds)
        self.time_before_than_or_equal_to_asserts(self.time_type_time_obj)

        self.assertTrue(self.time_type_time.before_than_or_equal_to(self.TEST_TIME_NO_SECONDS))

        test_time = time(self.TEST_TIME_OBJ.hour, self.TEST_TIME_OBJ.minute, self.TEST_TIME_OBJ.second + 1)
        self.assertTrue(self.time_type_time.before_than_or_equal_to(test_time))
